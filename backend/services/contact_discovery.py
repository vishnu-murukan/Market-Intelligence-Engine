import json
from services.json_utils import safe_json_parse
import re
import concurrent.futures
from typing import List, Dict, Any
from services.gemini import call_gemini_with_search
from services.cache_service import cache_service


class ContactDiscoveryService:
    @staticmethod
    def discover_contacts(brands: List[str], api_key: str, timeout: int = 45) -> List[Dict[str, Any]]:
        """
        Discover real decision-maker contacts for the given brand list.

        FIX: Instead of one giant prompt for all 10 brands (which always times out
        at 20s), we split into batches of 3 brands and run them in parallel.
        Each batch has its own 30s timeout, and results are merged.

        For each brand finds 2-3 senior stakeholders with:
          - name, role, brand_name
          - email    : real email from press page / company site / web search
          - linkedin : full profile URL from LinkedIn search
          - phone    : public number where available
          - source_url: where this person's info was found
        """
        if not brands:
            return []

        cache_key = "_".join(sorted(brands))
        cached = cache_service.get(cache_key, "contacts")
        if cached and isinstance(cached, list) and len(cached) >= max(len(brands), 5):
            return cached

        # Split brands into batches of 3 for parallel execution
        BATCH_SIZE = 3
        batches = [brands[i:i + BATCH_SIZE] for i in range(0, len(brands), BATCH_SIZE)]

        def fetch_batch(batch: List[str]) -> List[Dict[str, Any]]:
            brands_str = ", ".join(batch)
            prompt = f"""You are a senior B2B sales researcher with real-time web access.
Search the web RIGHT NOW to find real, verified decision-maker contacts at these companies:
{brands_str}

For EACH company, find 2-3 senior stakeholders relevant to a marketing/brand agency pitch.
Target roles: CMO, VP Marketing, Head of Brand, Marketing Director, Head of Partnerships,
Chief Brand Officer, or CEO/Founder for smaller brands.

SEARCH INSTRUCTIONS FOR EACH CONTACT:

LINKEDIN PROFILE (CRITICAL):
- Search: "[person full name] [company name] LinkedIn"
- You MUST return the actual LinkedIn profile URL in format: https://www.linkedin.com/in/username-slug
- Example: https://www.linkedin.com/in/johndoe/ or https://www.linkedin.com/in/john-doe-123456/
- If you cannot find the exact profile, search "[person name] [role] LinkedIn" as fallback
- Do NOT guess URLs — only return URLs you actually found via search

EMAIL ADDRESS (CRITICAL):
- Search: "[company name] press contact email" or "[company name] media contact"
- Check company website footer, /contact, /press, /newsroom pages
- Look for patterns: press@company.com, media@company.com, hello@company.com
- For the person specifically: try firstname@company.com or firstname.lastname@company.com
- A department email (press@, media@, marketing@) is acceptable if personal email isn't public
- Only write 'Not publicly listed' as absolute last resort

For EVERY contact return ALL fields:
1. brand_name      : Exact company name from the list
2. name            : Full real name (first and last)
3. role            : Current exact job title
4. email           : Real email address found via web search (see instructions above)
5. linkedin        : Full LinkedIn profile URL (see instructions above)
6. phone           : Company phone from website, or 'Not publicly listed'
7. source_url      : URL where you verified this person exists (LinkedIn, company team page, press release)
8. confidence_label: HIGH / MEDIUM / LOW

Return contacts for ALL {len(batch)} companies. Return ONLY a valid JSON array. No markdown.

[
  {{
    "brand_name": "Company Name",
    "name": "Full Name",
    "role": "Job Title",
    "email": "real@email.com",
    "linkedin": "https://www.linkedin.com/in/actual-profile-slug",
    "phone": "+1-555-000-0000",
    "source_url": "https://company.com/about/team",
    "confidence_label": "HIGH"
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
                if isinstance(result, list):
                    return result
                return []
            except Exception as e:
                print(f"[ContactDiscovery] Batch {batch} error: {e}")
                return []

        # Run all batches in parallel
        all_contacts: List[Dict[str, Any]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batches)) as executor:
            futures = {executor.submit(fetch_batch, batch): batch for batch in batches}
            for future in concurrent.futures.as_completed(futures, timeout=timeout):
                try:
                    batch_result = future.result()
                    all_contacts.extend(batch_result)
                    print(f"[ContactDiscovery] Batch done: {len(batch_result)} contacts.")
                except Exception as e:
                    print(f"[ContactDiscovery] A batch future failed: {e}")

        if not all_contacts:
            return []

        # Sanitise: no empty strings — replace with 'Not publicly listed'
        for c in all_contacts:
            for field in ["email", "linkedin", "phone", "source_url"]:
                val = (c.get(field) or "").strip()
                if not val:
                    c[field] = "Not publicly listed"
            # Ensure brand_name and name are present
            if not c.get("brand_name"):
                c["brand_name"] = "Unknown"
            if not c.get("name"):
                c["name"] = "Unknown Contact"

        print(f"[ContactDiscovery] Total contacts found: {len(all_contacts)}")
        cache_service.set(cache_key, "contacts", all_contacts, 3 * 3600)
        return all_contacts