"""
Gemini 2.0 Flash API service — all section prompts and streaming logic.
contacts + decisionmakers use Google Search grounding for real web data.
"""
import requests
import json
import os
from typing import Generator

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

SECTION_ORDER = [
    "contacts", "outreach", "decisionmakers", "tracking",
    "overview", "market", "competitors", "research",
    "activity", "events", "watchouts"
]

SECTION_PROMPTS = {
    "overview": lambda co, cat, ag: f"""
You are a senior market analyst. Provide a concise, factual intelligence brief on ({co}) ({cat}).
Cover:
1. Core business model and revenue streams
2. Scale: estimated employees, revenue range, and key markets
3. Target customer segments with demographics
4. Geographic presence
5. Market positioning (premium / mass / challenger / disruptor)
6. Founding year and key milestones
Be specific and factual. Use short paragraphs. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "market": lambda co, cat, ag: f"""
Analyze the current market position of ({co}) , complete the sentence fully dont end in between , if dontknow hallucinate and compelte the whole sentence({cat}).
Cover:
1. Brand perception — how consumers and industry view the brand
2. Estimated market share or category rank
3. Key competitive advantages and moats
4. Strategic shifts in the last 12 months
5. Any positioning evolution or pivots
6. SWOT summary (2 bullet points each)
Be specific with data points where available.Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "competitors": lambda co, cat, ag: f"""
You are a senior market analyst. List 4-5 direct competitors of ({co}) ({cat}).
For each competitor write a short section in plain text using this format:

Competitor Name
Strength: one short phrase describing their biggest advantage
Gap: one short phrase describing their biggest weakness
Strategy: 1-2 sentences on their current brand and marketing approach
Recent Activity: one recent campaign, product, or initiative

Separate each competitor with a blank line. No JSON, no bullet symbols, no markdown formatting.Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "research": lambda co, cat, ag: f"""
Produce a deep market intelligence brief on ({co}) ({cat}) for a marketing/branding agency,complete the sentence fully dont end in between , if dontknow hallucinate and compelte the whole sentence.
Cover each area with detail:

1. BRAND HEALTH SIGNALS — perception trends, sentiment, NPS signals, share of voice
2. CATEGORY MACRO-TRENDS — forces shaping this category in the next 12-24 months
3. AUDIENCE INSIGHTS — primary and secondary audience profiles, behavioral shifts, platform preference
4. DIGITAL & SOCIAL PRESENCE — platform strengths, estimated follower scale, content performance signals
5. CONTENT STRATEGY SIGNALS — tone, recurring themes, formats, what resonates
6. MARKETING SPEND SIGNALS — estimated media investment, channels prioritized, seasonality
7. AGENCY OPPORTUNITY — where a branding agency can add most value right now, specific gaps observed

Be detailed, insightful, and actionable for agency pitching.Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "activity": lambda co, cat, ag: f"""
Summarize all notable brand and marketing activity by ({co}) ({cat}) in the last 12-24 months. Add everything available with you and complete the sentence properly by collecting evry information. Dont miss out anything,
small number of hallucination is also acceptable, just fill the boxes with some kind of answer you get from you.
Format as a timeline. For each item include:
- Approximate date/period
- Activity type (campaign / launch / partnership / rebrand / media)
- Brief description with specific names where known
- Estimated scale or reach if available

Cover: campaigns, product launches, rebrands, ambassador deals, major media spends, agency changes, PR moments. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "events": lambda co, cat, ag: f"""
Describe the experiential marketing and events footprint of ({co}) ({cat}).
Include:
- Events hosted or co-hosted (names, formats, scale)
- Major sponsorships and brand activations
- Pop-ups, IRL experiences, retail activations
- Digital-physical hybrid events
- Frequency of activity (once a year? quarterly?)
- Notable outcomes or press coverage
- Gaps or white spaces — where experiential investment is low or missing

Be specific. Note any flagship annual properties they own. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "watchouts": lambda co, cat, ag: f"""
You are a senior marketing strategist. List 5 strategic watchouts, risks, tensions, or blind spots about ({co}) ({cat}) that a marketing/branding agency must know before engaging them.
Think: internal org dynamics, budget constraints, brand sensitivities, past agency relationships, category risks,complete the sentence fully dont end in between , if dontknow hallucinate and compelte the whole sentence

For each watchout write a short section in plain text using this format:

Watchout Title
2-3 sentences explaining the risk, tension, or insight the agency needs to know.

Separate each watchout with a blank line. Number them 1 through 5. No JSON, no bullet symbols, no markdown. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "decisionmakers": lambda co, cat, ag: f"""
You are a senior marketing strategist. Search the web and find the actual current decision-makers at ({co}) ({cat}) who are most relevant for a marketing/branding agency to approach.

Search for: "({co}) CMO", "({co}) VP Marketing", "({co}) Head of Brand", "({co}) marketing director LinkedIn" to find real names.

For each person write a short section in plain text using this format:

Full Name
Title: exact role title
Department: department name
Seniority: C-Suite / VP / Director / Manager
LinkedIn: their actual LinkedIn URL or profile slug if found
Why They Matter: 1-2 sentences on why this person is relevant for agency outreach
Pitch Angle: 1 sentence on what specific angle would resonate with them personally

Find 4 real people. Separate each with a blank line. No JSON, no bullet symbols, no markdown. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "contacts": lambda co, cat, ag: f"""
You are a research analyst. Search the web right now to find real, verified contact and social media information for ({co}) ({cat}).

Search for the following and report what you actually find:

OFFICIAL WEBSITE
Find and state the exact official website URL of darwinbox company.

SOCIAL MEDIA ACCOUNTS
Search for and list their actual verified social media handles and URLs:
- Instagram: search "({co}) Instagram official"
- LinkedIn: search "({co}) LinkedIn company page"
- Twitter/X: search "({co}) Twitter official"
- YouTube: search "({co}) YouTube channel"
- Facebook: search "({co}) Facebook page"
List the actual URLs you find, not guesses.

EMAIL FORMAT
Search for darwinbox company press contact email" or darwinbox company marketing contact" and report any real email addresses found.
Also state the most likely email domain based on their website.

PRESS & MEDIA CONTACT
Search for "({co}) press room" or "({co}) media contact" and report any real press contact pages or emails found.

LINKEDIN COMPANY PAGE
Find and state the exact LinkedIn company page URL for ({co}).

Only report information you actually find via search. If something is not found, say "Not found via search". Do not make up URLs or handles. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "outreach": lambda co, cat, ag: f"""
You are a senior marketing strategist. Create personalized outreach copy for a marketing/branding agency approaching ({co}) ({cat}).
{f'Agency context: {ag}' if ag else 'Agency: specializes in brand strategy and experiential marketing.'}

Write each piece as plain text using this exact format:

LINKEDIN MESSAGE
Write the LinkedIn connection message here. Max 280 characters. Conversational tone. Reference something specific about their recent brand activity. End with a natural soft call to action. Do not start with Hi or Hello.

EMAIL SUBJECT
Write the email subject line here. Max 8 words. Specific to their brand context. Creates curiosity. No "quick question" or "following up".

EMAIL BODY
Write the email body here. 150-200 words. Professional but warm. Open with a specific observation about their brand. Propose one concrete opportunity angle. End with a low-friction call to action. Sign as [Your Name], [Agency Name].

FOLLOW-UP LINKEDIN (Day 5)
Write the follow-up LinkedIn message here. 1-2 sentences. Add a new insight or data point, not just "following up".

FOLLOW-UP EMAIL SUBJECT (Day 8)
Write the follow-up email subject line here.

FOLLOW-UP EMAIL BODY (Day 8)
Write the follow-up email body here. 80-100 words. Reference something new such as a news item, campaign, or insight. Re-pitch softly.

No JSON, no markdown, no extra commentary. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst.""",

    "tracking": lambda co, cat, ag: f"""
Design a practical outreach tracking and measurement system for a marketing/branding agency targeting ({co}) ({cat}).

Structure your response with these exact sections:

UTM PARAMETERS
Provide the exact UTM string to append to all outreach links for ({co}).

EMAIL TRACKING APPROACH
Practical methods: open pixel tracking, link click tracking, reply detection. Include tool recommendations.

CRM FIELDS TO LOG
List exactly which fields to track for each contact in this campaign.

FOLLOW-UP CADENCE
Day-by-day sequence: Day 1 / Day 5 / Day 10 / Day 21 / Day 35. What to do on each day.

SUCCESS METRICS
5 specific KPIs to measure this campaign's effectiveness with target benchmarks.

QUALIFICATION SIGNALS
List 5 behavioral signals that indicate a lead is warming up and worth escalating.

WEEKLY REPORTING SNAPSHOT
A simple weekly metrics template your team should fill in.

Be specific and immediately usable. Don't use unwanted * , # in between the answers. keep it brief and presetable in a frontend, a structured format as a analyst."""
}


# ── Sections that use Google Search grounding for real web data ───────────────
SEARCH_SECTIONS = {"contacts", "decisionmakers"}


def _parse_response(data: dict) -> str:
    """Extract and join all text parts from a Gemini response."""
    block = data.get("promptFeedback", {}).get("blockReason")
    if block:
        raise RuntimeError(f"Content blocked by Gemini: {block}")
    parts = (
        data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [])
    )
    text = "\n".join(p.get("text", "") for p in parts if p.get("text"))
    if not text:
        raise RuntimeError("Empty response from Gemini")
    return text.strip()


def call_gemini(prompt: str, api_key: str) -> str:
    """Standard Gemini call — no web search."""
    key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not key:
        raise ValueError("No Gemini API key provided")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0.4,
            "topP": 0.9
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT",   "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",  "threshold": "BLOCK_ONLY_HIGH"},
        ]
    }

    resp = requests.post(
        f"{GEMINI_URL}?key={key}",
        json=payload,
        timeout=60
    )

    if not resp.ok:
        try:
            err = resp.json()
            msg = err.get("error", {}).get("message", f"HTTP {resp.status_code}")
        except Exception:
            msg = f"HTTP {resp.status_code}"
        raise RuntimeError(f"Gemini API error: {msg}")

    return _parse_response(resp.json())


def call_gemini_with_search(prompt: str, api_key: str) -> str:
    """Gemini call with Google Search grounding — fetches real web data."""
    key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not key:
        raise ValueError("No Gemini API key provided")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0.2,   # Low temp for factual accuracy
            "topP": 0.9
        },
        "tools": [{"google_search": {}}],   # Real-time web grounding
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT",   "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",  "threshold": "BLOCK_ONLY_HIGH"},
        ]
    }

    resp = requests.post(
        f"{GEMINI_URL}?key={key}",
        json=payload,
        timeout=120  # Search adds latency; 10-brand queries need more time
    )

    if not resp.ok:
        try:
            err = resp.json()
            msg = err.get("error", {}).get("message", f"HTTP {resp.status_code}")
        except Exception:
            msg = f"HTTP {resp.status_code}"
        # Gracefully fall back to standard call if search not available on this tier
        if resp.status_code in (400, 403) or "tool" in msg.lower() or "not supported" in msg.lower():
            return call_gemini(prompt, api_key)
        raise RuntimeError(f"Gemini API error: {msg}")

    return _parse_response(resp.json())


def run_section(section_id: str, company: str, category: str,
                agency: str, api_key: str) -> str:
    """Run a single research section — uses search grounding for contacts & decisionmakers."""
    fn = SECTION_PROMPTS.get(section_id)
    if not fn:
        raise ValueError(f"Unknown section: {section_id}")
    prompt = fn(company, category, agency)
    if section_id in SEARCH_SECTIONS:
        return call_gemini_with_search(prompt, api_key)
    return call_gemini(prompt, api_key)


def stream_all_sections(company: str, category: str,
                        agency: str, api_key: str) -> Generator[str, None, None]:
    """
    Yield SSE-formatted strings for each section as it completes.
    """
    import uuid
    session_id = str(uuid.uuid4())

    yield f"event: session\ndata: {json.dumps({'sessionId': session_id})}\n\n"
    yield f"event: start\ndata: {json.dumps({'company': company, 'category': category, 'total': len(SECTION_ORDER)})}\n\n"

    for idx, section_id in enumerate(SECTION_ORDER):
        yield f"event: section_start\ndata: {json.dumps({'sectionId': section_id, 'index': idx})}\n\n"
        try:
            result = run_section(section_id, company, category, agency, api_key)
            yield f"event: section_done\ndata: {json.dumps({'sectionId': section_id, 'result': result, 'index': idx + 1, 'total': len(SECTION_ORDER)})}\n\n"
        except Exception as e:
            yield f"event: section_error\ndata: {json.dumps({'sectionId': section_id, 'error': str(e), 'index': idx + 1, 'total': len(SECTION_ORDER)})}\n\n"

    yield f"event: complete\ndata: {json.dumps({'sessionId': session_id, 'total': len(SECTION_ORDER)})}\n\n"