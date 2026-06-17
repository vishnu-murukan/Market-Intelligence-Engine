import json
import re
from typing import List, Dict, Any
from services.gemini import call_gemini


class OutreachGeneratorService:
    @staticmethod
    def generate_outreach(
        brands: List[Dict[str, Any]],
        personalizations: List[Dict[str, Any]],
        agency_specialty: str,
        api_key: str,
        sender_info: Dict[str, str] = None,
        contacts: List[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate ready-to-send LinkedIn messages and cold emails per brand.

        Each item returned includes:
          linkedin_message  — under 300 chars, references brand context + pitch_hook
          linkedin_url      — deep-link to LinkedIn compose with message pre-filled
          email_subject     — high-open-rate subject line
          email_body        — complete 120-150 word email, signed with sender details
          email_cta         — standalone CTA sentence
          mailto_link       — mailto: href with To:, Subject:, Body: all pre-filled
          contact_email     — recipient email from contacts list (or '' if not found)
          sender_*          — sender fields echoed for frontend display
        """
        if not brands:
            return []

        # ── Sender details ────────────────────────────────────────────────────
        si = sender_info or {}
        sender_name    = si.get("sender_name", "").strip()
        sender_email   = si.get("sender_email", "").strip()
        sender_company = si.get("sender_company", "").strip()
        sender_title   = si.get("sender_title", "").strip()

        first_name = sender_name.split()[0] if sender_name else "the StepOne team"

        signature_block = "\n".join(filter(None, [
            sender_name,
            sender_title,
            sender_company,
            sender_email,
        ])) or "The StepOne Team"

        agency = agency_specialty or "brand strategy, experiential marketing, digital growth"

        # ── Build contact email lookup: brand_name -> best real email ─────────
        contact_email_map: Dict[str, str] = {}
        contact_name_map: Dict[str, str] = {}
        if contacts:
            for c in contacts:
                bname = (c.get("brand_name") or "").strip()
                email = (c.get("email") or "").strip()
                name  = (c.get("name") or "").strip()
                if bname and email and "@" in email and "not publicly" not in email.lower():
                    if bname not in contact_email_map:
                        contact_email_map[bname] = email
                        contact_name_map[bname] = name

        # ── Build rich Gemini payload ─────────────────────────────────────────
        payload = []
        for b in brands:
            b_name = b.get("brand_name", "")
            p = next((x for x in personalizations if x.get("brand_name") == b_name), {})
            payload.append({
                "brand_name": b_name,
                "why_now": b.get("why_now", ""),
                "why_stepone": b.get("why_stepone", ""),
                "opportunity_angle": p.get("opportunity_angle", ""),
                "pitch_hook": p.get("pitch_hook", ""),
                "urgency_level": p.get("urgency_level", "MEDIUM"),
                "recommended_service": p.get("recommended_service", ""),
                "contact_name": contact_name_map.get(b_name, ""),
            })

        prompt = f"""You are a senior outreach copywriter at StepOne agency ({agency}).
Write personalized, ready-to-send outreach for each brand below.

Sender (use their real details — NEVER use placeholders like [Your Name]):
  Name:    {sender_name or 'StepOne Team'}
  Title:   {sender_title or 'Agency Partner'}
  Company: {sender_company or 'StepOne'}
  Email:   {sender_email or 'hello@stepone.agency'}

Brands:
{json.dumps(payload, indent=2)}

For each brand produce:

1. brand_name
2. linkedin_message: Warm LinkedIn connection request. STRICTLY under 300 characters.
   - Open with the pitch_hook or a reference to the brand's recent activity.
   - Mention {sender_company or 'StepOne'} and the recommended_service briefly.
   - End with the sender's first name: "{first_name}".
   - Zero placeholders.
3. email_subject: 6-8 word subject line that references the brand or their recent move.
4. email_body: Complete cold email (120-150 words).
   - Para 1 (2 sentences): Specific hook referencing their recent activity or growth signal.
   - Para 2 (2-3 sentences): Propose the recommended_service using the opportunity_angle.
     Name a concrete outcome (e.g. "increase brand recall by 30%", "reach 2M new users").
   - Para 3 (1 sentence): The email_cta.
   - Blank line, then this exact signature:
{signature_block}
   - Use the contact's first name in the greeting if contact_name is provided.
   - ZERO placeholders — write as if sending today.
5. email_cta: One low-friction sentence (e.g. "Are you free for a 10-minute call Thursday?").

Return ONLY a valid JSON array. No markdown fences. No extra keys.

[
  {{
    "brand_name": "Brand Name",
    "linkedin_message": "Under-300-char draft",
    "email_subject": "Subject line",
    "email_body": "Full body with signature",
    "email_cta": "CTA sentence"
  }}
]
"""

        try:
            raw = call_gemini(prompt, api_key)
            clean = raw.strip()
            if clean.startswith("```"):
                clean = re.sub(r"^```(?:json)?\n", "", clean)
                clean = re.sub(r"\n```$", "", clean)
            outreach = json.loads(clean.strip())
        except Exception as e:
            print(f"[OutreachGenerator] Error: {e}")
            outreach = [
                {
                    "brand_name": b.get("brand_name"),
                    "linkedin_message": (
                        f"Hi — I've been tracking {b.get('brand_name')} and see a strong fit with "
                        f"what we do at {sender_company or 'StepOne'}. Would love to connect, {first_name}."
                    )[:300],
                    "email_subject": f"A brand idea for {b.get('brand_name')}",
                    "email_body": (
                        f"Hi,\n\nI came across {b.get('brand_name')} and was impressed by your recent momentum.\n\n"
                        f"At {sender_company or 'StepOne'} we specialise in {agency}. "
                        f"Based on your current trajectory, I believe we can help accelerate growth significantly.\n\n"
                        f"Would you be open to a quick 15-minute intro call?\n\n{signature_block}"
                    ),
                    "email_cta": "Are you free for a quick call this week?",
                }
                for b in brands
            ]

        # ── Post-process ──────────────────────────────────────────────────────
        for item in outreach:
            brand = item.get("brand_name", "")

            # Enforce LinkedIn 300-char hard limit
            li = item.get("linkedin_message", "")
            if len(li) > 300:
                item["linkedin_message"] = li[:297] + "..."

            # LinkedIn compose deep-link — auto-copies message on click (handled in frontend)
            item["linkedin_url"] = (
                "https://www.linkedin.com/messaging/compose/?body="
                + _url_encode(item["linkedin_message"])
            )

            # Resolve recipient email from contacts
            recipient_email = contact_email_map.get(brand, "")
            item["contact_email"] = recipient_email
            item["contact_name"]  = contact_name_map.get(brand, "")

            # Append CTA to body if missing
            full_body = item.get("email_body", "")
            cta = item.get("email_cta", "")
            if cta and cta not in full_body:
                full_body = full_body.rstrip() + f"\n\n{cta}"
                item["email_body"] = full_body

            # mailto: pre-fills To:, Subject:, Body:
            item["mailto_link"] = (
                f"mailto:{_url_encode(recipient_email)}"
                f"?subject={_url_encode(item.get('email_subject', ''))}"
                f"&body={_url_encode(full_body)}"
            )

            # Attach sender details for frontend display
            item["sender_name"]    = sender_name
            item["sender_email"]   = sender_email
            item["sender_company"] = sender_company
            item["sender_title"]   = sender_title

        return outreach


def _url_encode(text: str) -> str:
    from urllib.parse import quote
    return quote(str(text), safe="")