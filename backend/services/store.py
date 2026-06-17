"""
In-memory data store.
Replace with SQLite / PostgreSQL for production.
"""
import uuid
from datetime import datetime
from typing import Optional

# ── Storage ──────────────────────────────────────────────────────────────────
_sessions   = {}   # session_id -> dict
_campaigns  = {}   # campaign_id -> dict
_leads      = {}   # lead_id -> dict


def _now():
    return datetime.utcnow().isoformat() + "Z"


# ── Sessions ──────────────────────────────────────────────────────────────────

def create_session(company: str, category: str, agency: str = "") -> str:
    sid = str(uuid.uuid4())
    _sessions[sid] = {
        "id": sid,
        "company": company,
        "category": category,
        "agency": agency,
        "results": {},
        "statuses": {},
        "createdAt": _now(),
        "updatedAt": _now(),
    }
    return sid


def get_session(sid: str) -> Optional[dict]:
    return _sessions.get(sid)


def update_session(sid: str, section_id: str, result: str, status: str):
    s = _sessions.get(sid)
    if not s:
        return
    s["results"][section_id] = result
    s["statuses"][section_id] = status
    s["updatedAt"] = _now()


def list_sessions(limit: int = 20) -> list:
    rows = sorted(_sessions.values(), key=lambda x: x["createdAt"], reverse=True)
    return [
        {
            "id": s["id"],
            "company": s["company"],
            "category": s["category"],
            "sectionsCompleted": sum(1 for v in s["statuses"].values() if v == "done"),
            "createdAt": s["createdAt"],
        }
        for s in rows[:limit]
    ]


# ── Campaigns ─────────────────────────────────────────────────────────────────

def create_campaign(company: str, session_id: str = "") -> str:
    cid = str(uuid.uuid4())
    _campaigns[cid] = {
        "id": cid,
        "company": company,
        "sessionId": session_id,
        "leadIds": [],
        "stats": {"sent": 0, "opened": 0, "clicked": 0, "replied": 0, "meetings": 0},
        "createdAt": _now(),
    }
    return cid


def get_campaign(cid: str) -> Optional[dict]:
    return _campaigns.get(cid)


def list_campaigns() -> list:
    return sorted(_campaigns.values(), key=lambda x: x["createdAt"], reverse=True)


def _recalc_stats(cid: str):
    c = _campaigns.get(cid)
    if not c:
        return
    leads = [_leads[lid] for lid in c["leadIds"] if lid in _leads]
    c["stats"] = {
        "sent":     len(leads),
        "opened":   sum(1 for l in leads if l["status"] in ("Opened", "Clicked", "Replied", "Meeting Booked")),
        "clicked":  sum(1 for l in leads if l["status"] in ("Clicked", "Replied", "Meeting Booked")),
        "replied":  sum(1 for l in leads if l["status"] in ("Replied", "Meeting Booked")),
        "meetings": sum(1 for l in leads if l["status"] == "Meeting Booked"),
    }


# ── Leads ─────────────────────────────────────────────────────────────────────

def log_outreach(campaign_id: str, contact: str, channel: str, status: str,
                 email: str = "", title: str = "", notes: str = "") -> dict:
    lid = str(uuid.uuid4())
    lead = {
        "id": lid,
        "campaignId": campaign_id,
        "contact": contact,
        "email": email,
        "title": title,
        "channel": channel,
        "status": status,
        "notes": notes,
        "log": [{"status": status, "timestamp": _now(), "notes": notes}],
        "createdAt": _now(),
        "updatedAt": _now(),
    }
    _leads[lid] = lead
    c = _campaigns.get(campaign_id)
    if c:
        c["leadIds"].append(lid)
    _recalc_stats(campaign_id)
    return lead


def update_lead(lead_id: str, status: str, notes: str = "") -> Optional[dict]:
    lead = _leads.get(lead_id)
    if not lead:
        return None
    lead["status"] = status
    if notes:
        lead["notes"] = notes
    lead["updatedAt"] = _now()
    lead["log"].append({"status": status, "timestamp": _now(), "notes": notes})
    _recalc_stats(lead["campaignId"])
    return lead


def get_campaign_leads(campaign_id: str) -> list:
    c = _campaigns.get(campaign_id)
    if not c:
        return []
    return [_leads[lid] for lid in c["leadIds"] if lid in _leads]


def campaign_stats(campaign_id: str) -> dict:
    c = _campaigns.get(campaign_id)
    if not c:
        return {}
    s = c["stats"]
    return {
        **s,
        "responseRate": round((s["replied"] / s["sent"]) * 100) if s["sent"] else 0,
        "openRate":     round((s["opened"]  / s["sent"]) * 100) if s["sent"] else 0,
    }
