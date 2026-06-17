import json
from services.json_utils import safe_json_parse
import re
import concurrent.futures
from typing import List, Dict, Any
from services.gemini import call_gemini_with_search
from services.cache_service import cache_service


class RecentActivityService:
    @staticmethod
    def get_recent_activity(brands: List[str], api_key: str, timeout: int = 45) -> List[Dict[str, Any]]:
        """
        Discover recent brand activity for all brands.

        FIX: Batches brands into groups of 4 and runs in parallel.
        The old single-prompt approach for 10 brands always hit the 15s timeout.
        Each batch gets its own 30s window; results are merged.
        """
        if not brands:
            return []

        cache_key = "_".join(sorted(brands))
        cached = cache_service.get(cache_key, "activities")
        if cached and isinstance(cached, list) and len(cached) >= max(len(brands), 3):
            return cached

        BATCH_SIZE = 4
        batches = [brands[i:i + BATCH_SIZE] for i in range(0, len(brands), BATCH_SIZE)]

        def fetch_batch(batch: List[str]) -> List[Dict[str, Any]]:
            brands_str = ", ".join(batch)
            prompt = f"""You are a senior business journalist with real-time web access.

Search the web RIGHT NOW for recent activities for these brands: {brands_str}

Find funding rounds, product launches, rebrands, major campaigns, partnerships,
expansions, executive hires, or press-worthy moments from the last 12-24 months.

For EACH brand provide 1-2 of their most significant recent activities:

1. brand_name      : Exact brand name from the list.
2. activity        : 2-3 sentence description of what happened, why it matters,
                     and what it signals about the brand's direction.
3. activity_type   : One of: "Funding", "Product Launch", "Campaign", "Partnership",
                     "Expansion", "Rebrand", "Executive Hire", "Other".
4. date            : Month and Year (e.g. "March 2026").
5. impact_on_brand : 1 sentence — what this means for the brand's growth trajectory.
6. source_url      : Official press release, news article, or company blog URL.
7. confidence_score: "HIGH", "MEDIUM", or "LOW".

RULES:
- Return activities for ALL {len(batch)} brands listed.
- Search the web — do not rely solely on training data.
- If a brand has no public activity in the last 24 months, say so honestly in the activity field
  rather than fabricating something.

Return ONLY a valid JSON array. No markdown. No preamble.

[
  {{
    "brand_name": "Example Co",
    "activity": "Example Co raised a $50M Series B led by Sequoia to expand into the European market.",
    "activity_type": "Funding",
    "date": "January 2026",
    "impact_on_brand": "Signals aggressive international expansion and increased marketing budget.",
    "source_url": "https://techcrunch.com/example-series-b",
    "confidence_score": "HIGH"
  }}
]
"""
            try:
                raw = call_gemini_with_search(prompt, api_key)
                clean = raw.strip()
                if clean.startswith("```"):
                    clean = re.sub(r"^```(?:json)?\n", "", clean)
                    clean = re.sub(r"\n```$", "", clean)
                result = safe_json_parse(clean)
                return result if isinstance(result, list) else []
            except Exception as e:
                print(f"[RecentActivity] Batch {batch} error: {e}")
                return []

        all_activities: List[Dict[str, Any]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batches)) as executor:
            futures = {executor.submit(fetch_batch, batch): batch for batch in batches}
            for future in concurrent.futures.as_completed(futures, timeout=timeout):
                try:
                    result = future.result()
                    all_activities.extend(result)
                    print(f"[RecentActivity] Batch done: {len(result)} activities.")
                except Exception as e:
                    print(f"[RecentActivity] Batch future failed: {e}")

        if all_activities:
            cache_service.set(cache_key, "activities", all_activities, 3 * 3600)

        print(f"[RecentActivity] Total: {len(all_activities)} activities for {len(brands)} brands.")
        return all_activities