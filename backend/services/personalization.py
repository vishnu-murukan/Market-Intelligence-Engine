import json
import re
from typing import List, Dict, Any
from services.gemini import call_gemini


class PersonalizationService:
    @staticmethod
    def personalize_opportunities(
        brands: List[Dict[str, Any]],
        activities: List[Dict[str, Any]],
        agency_specialty: str,
        api_key: str,
    ) -> List[Dict[str, Any]]:
        """
        Synthesize brand context + recent activity + event presence to generate
        a highly specific, personalised opportunity angle for each brand.

        FIX: Now uses all available brand signals — why_stepone, why_now,
        recent activities (with activity_type + impact), and event presence —
        instead of just the activity text. This produces angles that directly
        reference brand context, recent moves, and a concrete StepOne proposal.
        """
        if not brands:
            return []

        agency = agency_specialty or "brand strategy, experiential marketing, digital growth"

        # Build rich payload per brand
        brands_data = []
        for b in brands:
            b_name = b.get("brand_name", "")
            # Collect all activities for this brand with full context
            b_activities = []
            for a in activities:
                if a.get("brand_name") == b_name:
                    entry = a.get("activity", "")
                    atype = a.get("activity_type", "")
                    impact = a.get("impact_on_brand", "")
                    if atype:
                        entry += f" [{atype}]"
                    if impact:
                        entry += f" — {impact}"
                    b_activities.append(entry)

            brands_data.append({
                "brand_name": b_name,
                "why_stepone": b.get("why_stepone", ""),
                "why_now": b.get("why_now", ""),
                "source_url": b.get("source_url", ""),
                "strategic_fit_score": b.get("strategic_fit_score", ""),
                "growth_signal_score": b.get("growth_signal_score", ""),
                "recent_activities": b_activities,
            })

        prompt = f"""You are a senior new-business strategist at 'StepOne', a premium marketing agency
specialising in: {agency}.

Your job is to write a razor-sharp, specific "opportunity_angle" for StepOne to pitch to each brand.
This is NOT generic agency talk — each angle must:
  - Reference the brand's specific recent activity or growth signal.
  - Identify a precise gap or inflection point in their marketing or brand strategy.
  - Propose the exact type of campaign, activation, or service StepOne would offer.
  - Be written as if a senior strategist who has researched this brand deeply is presenting it
    to the StepOne sales team before a first call.

Brands Data:
{json.dumps(brands_data, indent=2)}

For each brand return:
1. brand_name        : Brand name (exact match).
2. opportunity_angle : 3-4 sentences covering:
     Sentence 1 — What the brand recently did or is going through (reference specific activity).
     Sentence 2 — What gap or opportunity this creates for a marketing agency.
     Sentence 3 — Exactly what StepOne would propose (campaign type, activation, channel mix).
     Sentence 4 — The measurable outcome or business impact StepOne would deliver.
3. pitch_hook        : A single punchy sentence (max 15 words) that could open a cold call or
                       LinkedIn message — specific, not generic.
4. urgency_level     : "HIGH", "MEDIUM", or "LOW" based on how time-sensitive the opportunity is.
5. recommended_service: The primary StepOne service this brand needs most right now
                        (e.g. "Brand Refresh", "Experiential Campaign", "Digital Growth Sprint",
                        "Content Strategy", "Influencer Programme", "Launch Campaign", etc.)

Return ONLY a valid JSON array. No markdown. No preamble.

[
  {{
    "brand_name": "Brand Name",
    "opportunity_angle": "Since Brand X recently launched Y...",
    "pitch_hook": "Your new Y launch needs a campaign that makes noise globally.",
    "urgency_level": "HIGH",
    "recommended_service": "Launch Campaign"
  }}
]
"""

        try:
            raw_response = call_gemini(prompt, api_key)
            clean_text = raw_response.strip()
            if clean_text.startswith("```"):
                clean_text = re.sub(r"^```(?:json)?\n", "", clean_text)
                clean_text = re.sub(r"\n```$", "", clean_text)
            personalizations = json.loads(clean_text.strip())
            return personalizations
        except Exception as e:
            print(f"[PersonalizationService] Error: {e}")
            return [
                {
                    "brand_name": b.get("brand_name"),
                    "opportunity_angle": (
                        f"{b.get('brand_name')} is at an inflection point. "
                        f"{b.get('why_now', '')} "
                        f"StepOne can help with a targeted brand strategy engagement. "
                        f"This would unlock new audience reach and measurable brand equity growth."
                    ),
                    "pitch_hook": f"Your growth signals show it's the right time to invest in brand.",
                    "urgency_level": "MEDIUM",
                    "recommended_service": "Brand Strategy",
                }
                for b in brands
            ]