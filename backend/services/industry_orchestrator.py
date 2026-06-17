import json
from services.json_utils import safe_json_parse
import time
import re
import concurrent.futures
from typing import Generator, List, Dict, Any

from services.brand_discovery import BrandDiscoveryService
from services.event_discovery import EventDiscoveryService
from services.contact_discovery import ContactDiscoveryService
from services.recent_activity import RecentActivityService
from services.personalization import PersonalizationService
from services.outreach_generator import OutreachGeneratorService
from services.confidence_scoring import ConfidenceScoringService
from services.demo_mode import is_demo_mode_triggered, get_demo_data
from services.cache_service import cache_service
from services.store import create_session, update_session


class IndustryOrchestrator:
    @staticmethod
    def stream_pipeline(
        industry: str,
        agency_specialty: str,
        api_key: str,
        force_demo: bool = False,
        sender_name: str = "",
        sender_email: str = "",
        sender_company: str = "",
        sender_title: str = "",
    ) -> Generator[str, None, None]:
        """
        Full industry discovery pipeline — yields SSE events.
        Hierarchy: LIVE DATA -> Cache (only if >= 10 brands) -> Demo -> Empty.
        """
        session_id = create_session(industry, "Industry: " + industry, agency_specialty)

        # FIX: removed the rogue `use_demo = False` line that was overriding logic below
        use_demo = force_demo or not api_key or api_key.strip() == ""
        is_demo_available = is_demo_mode_triggered(industry)

        brands: List[Dict[str, Any]] = []
        events: List[Dict[str, Any]] = []
        contacts: List[Dict[str, Any]] = []
        activities: List[Dict[str, Any]] = []
        personalizations: List[Dict[str, Any]] = []
        outreach: List[Dict[str, Any]] = []
        final_report: Dict[str, Any] = {}

        sender_info = {
            "sender_name": sender_name,
            "sender_email": sender_email,
            "sender_company": sender_company,
            "sender_title": sender_title,
        }

        # ─── CASE A: DEMO MODE ────────────────────────────────────────────────
        if use_demo:
            if is_demo_available:
                source_mode = "CACHED VERIFIED DATA"
                yield f"event: session\ndata: {json.dumps({'sessionId': session_id, 'sourceMode': source_mode})}\n\n"
                yield f"event: start\ndata: {json.dumps({'company': industry, 'category': 'Industry Discovery', 'total': 6})}\n\n"

                demo_data = get_demo_data(industry)
                stages = ["brands", "events", "contacts", "activity", "outreach", "scores"]
                for stage in stages:
                    yield f"event: section_start\ndata: {json.dumps({'sectionId': stage, 'demoMode': True, 'sourceMode': source_mode})}\n\n"
                    time.sleep(0.8)
                    if stage == "brands":
                        brands = demo_data.get("brands", [])
                        update_session(session_id, "brands", json.dumps(brands), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'brands', 'result': brands, 'index': 1, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    elif stage == "events":
                        events = demo_data.get("events", [])
                        update_session(session_id, "events", json.dumps(events), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'events', 'result': events, 'index': 2, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    elif stage == "contacts":
                        contacts = demo_data.get("contacts", [])
                        update_session(session_id, "contacts", json.dumps(contacts), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'contacts', 'result': contacts, 'index': 3, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    elif stage == "activity":
                        activities = demo_data.get("activities", [])
                        update_session(session_id, "activity", json.dumps(activities), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'activity', 'result': activities, 'index': 4, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    elif stage == "outreach":
                        personalizations = PersonalizationService.personalize_opportunities(
                            brands, activities, agency_specialty, api_key)
                        outreach = OutreachGeneratorService.generate_outreach(
                            brands, personalizations, agency_specialty, api_key,
                            sender_info=sender_info, contacts=contacts)
                        update_session(session_id, "outreach", json.dumps(outreach), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'outreach', 'result': outreach, 'index': 5, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    elif stage == "scores":
                        final_report = ConfidenceScoringService.score_and_rank(
                            brands, events, contacts, activities, outreach)
                        final_report["sourceMode"] = source_mode
                        update_session(session_id, "scores", json.dumps(final_report), "done")
                        update_session(session_id, "industry_report", json.dumps(final_report), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'scores', 'result': final_report, 'index': 6, 'total': 6, 'sourceMode': source_mode})}\n\n"

                yield f"event: complete\ndata: {json.dumps({'sessionId': session_id, 'total': 6})}\n\n"
                return
            else:
                source_mode = "LIMITED PUBLIC DATA AVAILABLE"
                yield f"event: session\ndata: {json.dumps({'sessionId': session_id, 'sourceMode': source_mode})}\n\n"
                yield f"event: start\ndata: {json.dumps({'company': industry, 'category': 'Industry Discovery', 'total': 6})}\n\n"
                for idx, stage in enumerate(["brands", "events", "contacts", "activity", "outreach", "scores"]):
                    yield f"event: section_start\ndata: {json.dumps({'sectionId': stage, 'sourceMode': source_mode})}\n\n"
                    if stage == "scores":
                        final_report = {"prospects": [], "events": [], "contacts": [], "activities": [], "outreach": [], "sourceMode": source_mode}
                        update_session(session_id, "scores", json.dumps(final_report), "done")
                        update_session(session_id, "industry_report", json.dumps(final_report), "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'scores', 'result': final_report, 'index': 6, 'total': 6, 'sourceMode': source_mode})}\n\n"
                    else:
                        update_session(session_id, stage, "[]", "done")
                        yield f"event: section_done\ndata: {json.dumps({'sectionId': stage, 'result': [], 'index': idx + 1, 'total': 6, 'sourceMode': source_mode})}\n\n"
                yield f"event: complete\ndata: {json.dumps({'sessionId': session_id, 'total': 6})}\n\n"
                return

        # ─── CASE B: LIVE MODE ────────────────────────────────────────────────
        source_mode = "LIVE DATA"
        yield f"event: session\ndata: {json.dumps({'sessionId': session_id, 'sourceMode': source_mode})}\n\n"
        yield f"event: start\ndata: {json.dumps({'company': industry, 'category': 'Industry Discovery', 'total': 6})}\n\n"

        # STAGE 1: Brand Discovery
        # FIX: Bust stale cache with fewer than 10 brands BEFORE attempting live call
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'brands', 'sourceMode': source_mode})}\n\n"

        cached_brands = cache_service.get(industry, "brands")
        if cached_brands and isinstance(cached_brands, list) and len(cached_brands) < 10:
            print(f"[Orchestrator] Busting stale brand cache ({len(cached_brands)} entries) for '{industry}'.")
            cache_service.invalidate(industry, "brands")
            cached_brands = None

        try:
            from services.gemini import call_gemini_with_search

            prompt = f"""You are a senior market research analyst.
Search the web right now to find EXACTLY 10 real, verified, currently active companies/brands
in the "{industry}" industry.

You MUST return exactly 10 items. Do not stop at 5. Do not truncate early.
Count your items before returning — if you have fewer than 10, add more before finishing.

For each company:
1. brand_name            : Official company name.
2. why_stepone           : 1-2 sentences why StepOne agency (brand strategy, digital experience,
                           marketing) is a great partner.
3. why_now               : 1-2 sentences why they need marketing services right now.
4. strategic_fit_score   : 1-100
5. growth_signal_score   : 1-100
6. event_presence_score  : 1-100
7. recent_activity_score : 1-100
8. confidence_score      : 1-100
9. source_url            : Official homepage URL.

Return ONLY a valid JSON array of exactly 10 objects.
No markdown fences. No preamble. Only the JSON array.
"""
            raw_response = call_gemini_with_search(prompt, api_key)
            clean_text = raw_response.strip()
            if clean_text.startswith("```"):
                clean_text = re.sub(r"^```(?:json)?\n", "", clean_text)
                clean_text = re.sub(r"\n```$", "", clean_text)

            parsed = safe_json_parse(clean_text)
            if isinstance(parsed, list) and len(parsed) >= 5:
                brands = parsed[:10]
                cache_service.set(industry, "brands", brands, 6 * 3600)
                print(f"[Orchestrator] Live brand discovery: {len(brands)} brands.")
            else:
                raise ValueError(f"Only {len(parsed) if isinstance(parsed, list) else 0} brands returned")

        except Exception as e:
            print(f"[Orchestrator] Live brand call failed ({type(e).__name__}: {e}). Checking cache...")
            brands = cache_service.get(industry, "brands") or []
            if brands:
                source_mode = "CACHED VERIFIED DATA"
                print(f"[Orchestrator] Cache fallback: {len(brands)} brands.")
            elif is_demo_available:
                brands = get_demo_data(industry).get("brands", [])
                source_mode = "CACHED VERIFIED DATA"
                print(f"[Orchestrator] Demo fallback: {len(brands)} brands.")
            else:
                try:
                    brands = BrandDiscoveryService.discover_brands(industry, api_key) or []
                except Exception as svc_err:
                    print(f"[Orchestrator] BrandDiscoveryService also failed: {svc_err}")
                    brands = []
                if not brands:
                    source_mode = "LIMITED PUBLIC DATA AVAILABLE"

        if not brands:
            source_mode = "LIMITED PUBLIC DATA AVAILABLE"
            update_session(session_id, "brands", "[]", "done")
            yield f"event: section_done\ndata: {json.dumps({'sectionId': 'brands', 'result': [], 'index': 1, 'total': 6, 'sourceMode': source_mode})}\n\n"
            for idx, stage in enumerate(["events", "contacts", "activity", "outreach", "scores"]):
                yield f"event: section_start\ndata: {json.dumps({'sectionId': stage, 'sourceMode': source_mode})}\n\n"
                if stage == "scores":
                    final_report = {"prospects": [], "events": [], "contacts": [], "activities": [], "outreach": [], "sourceMode": source_mode}
                    update_session(session_id, "scores", json.dumps(final_report), "done")
                    update_session(session_id, "industry_report", json.dumps(final_report), "done")
                    yield f"event: section_done\ndata: {json.dumps({'sectionId': 'scores', 'result': final_report, 'index': 6, 'total': 6, 'sourceMode': source_mode})}\n\n"
                else:
                    update_session(session_id, stage, "[]", "done")
                    yield f"event: section_done\ndata: {json.dumps({'sectionId': stage, 'result': [], 'index': idx + 2, 'total': 6, 'sourceMode': source_mode})}\n\n"
            yield f"event: complete\ndata: {json.dumps({'sessionId': session_id, 'total': 6})}\n\n"
            return

        update_session(session_id, "brands", json.dumps(brands), "done")
        yield f"event: section_done\ndata: {json.dumps({'sectionId': 'brands', 'result': brands, 'index': 1, 'total': 6, 'sourceMode': source_mode})}\n\n"

        brand_names = [b.get("brand_name") for b in brands if b.get("brand_name")]

        # STAGE 2, 3, 4: Parallel discovery
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'events', 'sourceMode': source_mode})}\n\n"
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'contacts', 'sourceMode': source_mode})}\n\n"
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'activity', 'sourceMode': source_mode})}\n\n"

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            event_future   = executor.submit(EventDiscoveryService.discover_events, industry, api_key, 60)
            # FIX: pass ALL 10 brand names; ContactDiscovery now batches internally
            contact_future = executor.submit(ContactDiscoveryService.discover_contacts, brand_names, api_key, 120)
            activity_future = executor.submit(RecentActivityService.get_recent_activity, brand_names, api_key, 60)

            concurrent.futures.wait([event_future, contact_future, activity_future])

            # Events
            try:
                events = event_future.result()
                if not events or (isinstance(events, list) and len(events) > 0 and "error" in events[0]):
                    events = cache_service.get(industry, "events") or []
                    if not events and is_demo_available:
                        events = get_demo_data(industry).get("events", [])
                        source_mode = "CACHED VERIFIED DATA"
                update_session(session_id, "events", json.dumps(events), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'events', 'result': events, 'index': 2, 'total': 6, 'sourceMode': source_mode})}\n\n"
            except Exception as e:
                print(f"[EventDiscovery] Error: {e}")
                events = get_demo_data(industry).get("events", []) if is_demo_available else []
                update_session(session_id, "events", json.dumps(events), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'events', 'result': events, 'index': 2, 'total': 6, 'sourceMode': source_mode})}\n\n"

            # Contacts
            try:
                contacts = contact_future.result()
                if not contacts or (isinstance(contacts, list) and len(contacts) > 0 and "error" in contacts[0]):
                    cache_key = "_".join(sorted(brand_names))
                    contacts = cache_service.get(cache_key, "contacts") or []
                    if not contacts and is_demo_available:
                        contacts = get_demo_data(industry).get("contacts", [])
                        source_mode = "CACHED VERIFIED DATA"
                update_session(session_id, "contacts", json.dumps(contacts), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'contacts', 'result': contacts, 'index': 3, 'total': 6, 'sourceMode': source_mode})}\n\n"
            except Exception as e:
                print(f"[ContactDiscovery] Error: {e}")
                contacts = get_demo_data(industry).get("contacts", []) if is_demo_available else []
                update_session(session_id, "contacts", json.dumps(contacts), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'contacts', 'result': contacts, 'index': 3, 'total': 6, 'sourceMode': source_mode})}\n\n"

            # Activities
            try:
                activities = activity_future.result()
                if not activities or (isinstance(activities, list) and len(activities) > 0 and "error" in activities[0]):
                    cache_key = "_".join(sorted(brand_names))
                    activities = cache_service.get(cache_key, "activities") or []
                    if not activities and is_demo_available:
                        activities = get_demo_data(industry).get("activities", [])
                        source_mode = "CACHED VERIFIED DATA"
                update_session(session_id, "activity", json.dumps(activities), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'activity', 'result': activities, 'index': 4, 'total': 6, 'sourceMode': source_mode})}\n\n"
            except Exception as e:
                print(f"[RecentActivity] Error: {e}")
                activities = get_demo_data(industry).get("activities", []) if is_demo_available else []
                update_session(session_id, "activity", json.dumps(activities), "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': 'activity', 'result': activities, 'index': 4, 'total': 6, 'sourceMode': source_mode})}\n\n"

        # STAGE 5: Outreach — pass contacts so mailto: uses real discovered emails
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'outreach', 'sourceMode': source_mode})}\n\n"
        try:
            personalizations = PersonalizationService.personalize_opportunities(
                brands, activities, agency_specialty, api_key)
            outreach = OutreachGeneratorService.generate_outreach(
                brands, personalizations, agency_specialty, api_key,
                sender_info=sender_info,
                contacts=contacts,  # real emails from ContactDiscovery flow into mailto:
            )
            update_session(session_id, "outreach", json.dumps(outreach), "done")
            yield f"event: section_done\ndata: {json.dumps({'sectionId': 'outreach', 'result': outreach, 'index': 5, 'total': 6, 'sourceMode': source_mode})}\n\n"
        except Exception as e:
            print(f"[OutreachGenerator] Error: {e}")
            update_session(session_id, "outreach", f"Error: {e}", "error")
            yield f"event: section_error\ndata: {json.dumps({'sectionId': 'outreach', 'error': str(e), 'sourceMode': source_mode})}\n\n"
            outreach = []

        # STAGE 6: Scores
        yield f"event: section_start\ndata: {json.dumps({'sectionId': 'scores', 'sourceMode': source_mode})}\n\n"
        try:
            final_report = ConfidenceScoringService.score_and_rank(brands, events, contacts, activities, outreach)
            final_report["sourceMode"] = source_mode
            update_session(session_id, "scores", json.dumps(final_report), "done")
            update_session(session_id, "industry_report", json.dumps(final_report), "done")
            yield f"event: section_done\ndata: {json.dumps({'sectionId': 'scores', 'result': final_report, 'index': 6, 'total': 6, 'sourceMode': source_mode})}\n\n"
        except Exception as e:
            print(f"[ConfidenceScoring] Error: {e}")
            update_session(session_id, "scores", f"Error: {e}", "error")
            yield f"event: section_error\ndata: {json.dumps({'sectionId': 'scores', 'error': str(e), 'sourceMode': source_mode})}\n\n"

        yield f"event: complete\ndata: {json.dumps({'sessionId': session_id, 'total': 6})}\n\n"