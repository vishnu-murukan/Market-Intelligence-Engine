import json
from services.json_utils import safe_json_parse
import re
import concurrent.futures
from typing import List, Dict, Any
from services.gemini import call_gemini_with_search
from services.cache_service import cache_service


class BrandDiscoveryService:
    @staticmethod
    def discover_brands(industry: str, api_key: str, timeout: int = 90) -> List[Dict[str, Any]]:
        """
        Discover exactly 10 brands in the specified industry.
        
        FIX: Cache is only used if it contains >= 10 brands.
        Stale caches with fewer entries are ignored so a fresh live
        call is always made when the cached data is insufficient.
        """
        # Check cache — but ONLY accept it if it has 10 brands
        # This is the root cause of the "5 companies" bug:
        # old caches with 5 entries were being served forever.
        cached = cache_service.get(industry, "brands")
        if cached and isinstance(cached, list) and len(cached) >= 10:
            return cached

        # If cache exists but has < 10 brands, bust it and re-fetch live
        if cached and isinstance(cached, list) and len(cached) < 10:
            print(f"[BrandDiscovery] Cache has only {len(cached)} brands for '{industry}' — busting and re-fetching.")
            cache_service.invalidate(industry, "brands")

        prompt = f"""You are a senior market research analyst.
Search the web right now to find EXACTLY 10 real, verified, and currently active
companies/brands operating in the "{industry}" industry.

You MUST return exactly 10 items in the JSON array — no more, no less.
Do not stop at 5. Do not truncate. Return all 10.

For each company evaluate:
1. brand_name            : Official company name.
2. why_stepone           : 1-2 sentences — compelling reason why StepOne agency (premium brand
                           strategy, digital experience, marketing) is a great partner.
3. why_now               : 1-2 sentences — why they need brand/marketing services right now.
4. strategic_fit_score   : 1-100, alignment with StepOne.
5. growth_signal_score   : 1-100, recent funding / hiring / expansion signals.
6. event_presence_score  : 1-100, conference / trade-show footprint.
7. recent_activity_score : 1-100, recent campaigns or press releases.
8. confidence_score      : 1-100, your confidence in this data.
9. source_url            : Official homepage URL.

Return ONLY a valid JSON array of exactly 10 objects.
No markdown fences. No preamble. No explanation. Just the JSON array.
If a particular company has limited public data, still include it with best-effort scores.

Required JSON format:
[
  {{
    "brand_name": "Example Brand",
    "why_stepone": "...",
    "why_now": "...",
    "strategic_fit_score": 85,
    "growth_signal_score": 90,
    "event_presence_score": 75,
    "recent_activity_score": 80,
    "confidence_score": 95,
    "source_url": "https://www.example.com"
  }}
]
"""

        def run_call():
            return call_gemini_with_search(prompt, api_key)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_call)
            try:
                raw_response = future.result(timeout=timeout)
                clean_text = raw_response.strip()
                if clean_text.startswith("```"):
                    clean_text = re.sub(r"^```(?:json)?\n", "", clean_text)
                    clean_text = re.sub(r"\n```$", "", clean_text)

                brands = safe_json_parse(clean_text)

                if not isinstance(brands, list):
                    print(f"[BrandDiscovery] Unexpected response type: {type(brands)}")
                    return []

                print(f"[BrandDiscovery] Gemini returned {len(brands)} brands for '{industry}'.")

                # Trim to 10 if Gemini over-delivered
                brands = brands[:10]

                if brands:
                    cache_service.set(industry, "brands", brands, 6 * 3600)

                return brands

            except concurrent.futures.TimeoutError:
                print(f"[BrandDiscovery] Timed out after {timeout}s for '{industry}'.")
                return [{"error": "Timed out", "status": "Timed out"}]
            except Exception as e:
                print(f"[BrandDiscovery] Error: {e}")
                return []