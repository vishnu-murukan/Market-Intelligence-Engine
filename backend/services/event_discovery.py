import json
from services.json_utils import safe_json_parse
import re
import concurrent.futures
from typing import List, Dict, Any
from services.gemini import call_gemini_with_search
from services.cache_service import cache_service


class EventDiscoveryService:
    @staticmethod
    def discover_events(industry: str, api_key: str, timeout: int = 30) -> List[Dict[str, Any]]:
        """
        Discover real upcoming industry events AND map them to known prospects.
        Returns minimum 5 events with full detail including which discovered
        brands are likely attending/sponsoring.
        """
        cached = cache_service.get(industry, "events")
        if cached and isinstance(cached, list) and len(cached) >= 3:
            return cached

        prompt = f"""You are a senior event marketing manager with access to the web.

Search the web RIGHT NOW for real, confirmed, upcoming industry conferences, summits,
trade shows, and expos in 2025, 2026, or 2027 for the "{industry}" industry.

Find at least 5 real events. For each event provide:

1. event_name              : Official name of the event.
2. date                    : Scheduled dates (e.g. "October 12-15, 2026").
3. location                : City, Country (or "Virtual").
4. official_url            : Official homepage URL — search and verify this is real.
5. description             : 1-2 sentences about what the event covers and who attends.
6. expected_attendance     : Approximate number of attendees if publicly stated.
7. sponsorship_available   : "Yes", "No", or "Unknown" — is brand/agency sponsorship available?
8. likely_participating_brands : Comma-separated list of 3-5 real companies in this space
                                 likely to attend, exhibit, or sponsor based on past years.
9. why_stepone_should_attend: 1 sentence — why a marketing agency like StepOne should
                               be present or use this event to approach prospects.
10. confidence_score       : "HIGH" (verified from official site), "MEDIUM", or "LOW".
11. source_url             : URL where you verified this event exists.

CRITICAL:
- Only return REAL events — do NOT fabricate names, dates, or URLs.
- Search "[industry] conference 2026", "[industry] summit 2026", "[industry] expo 2026".
- If an event has already passed in 2025, include it only if the 2026 edition is confirmed.
- Return at least 5 events. If fewer than 5 exist publicly, return what you find.

Return ONLY a valid JSON array. No markdown fences. No preamble.

[
  {{
    "event_name": "Example Summit 2026",
    "date": "September 14-16, 2026",
    "location": "Las Vegas, NV, USA",
    "official_url": "https://www.exampleevent.com",
    "description": "Annual summit bringing together 3,000 brand leaders and marketing executives.",
    "expected_attendance": "3,000+",
    "sponsorship_available": "Yes",
    "likely_participating_brands": "Brand A, Brand B, Brand C, Brand D",
    "why_stepone_should_attend": "Prime opportunity to meet CMOs from the top 50 brands in this space.",
    "confidence_score": "HIGH",
    "source_url": "https://www.exampleevent.com/about"
  }}
]
"""

        def run_call():
            return call_gemini_with_search(prompt, api_key)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_call)
            try:
                raw = future.result(timeout=timeout)
                clean = raw.strip()
                if clean.startswith("```"):
                    clean = re.sub(r"^```(?:json)?\n", "", clean)
                    clean = re.sub(r"\n```$", "", clean)

                events = safe_json_parse(clean)
                if isinstance(events, list) and len(events) > 0:
                    # Sanitise empty fields
                    for e in events:
                        for field in ["official_url", "source_url", "description",
                                      "expected_attendance", "sponsorship_available",
                                      "why_stepone_should_attend"]:
                            if not (e.get(field) or "").strip():
                                e[field] = "Not publicly listed"
                    cache_service.set(industry, "events", events, 24 * 3600)
                    return events
                return []
            except concurrent.futures.TimeoutError:
                print(f"[EventDiscovery] Timed out after {timeout}s.")
                return [{"error": "Timed out"}]
            except Exception as e:
                print(f"[EventDiscovery] Error: {e}")
                return []