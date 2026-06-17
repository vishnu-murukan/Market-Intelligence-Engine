from flask import Blueprint, request, jsonify
from services.store import (
    create_campaign, get_campaign, list_campaigns,
    log_outreach, update_lead, get_campaign_leads, campaign_stats
)

tracking_bp = Blueprint("tracking", __name__)


@tracking_bp.get("/campaigns")
def get_campaigns():
    return jsonify(list_campaigns())


@tracking_bp.post("/campaigns")
def post_campaign():
    data       = request.get_json(force=True)
    company    = (data.get("company")   or "").strip()
    session_id = (data.get("sessionId") or "").strip()
    if not company:
        return jsonify({"error": "company required"}), 400
    cid = create_campaign(company, session_id)
    return jsonify(get_campaign(cid)), 201


@tracking_bp.get("/campaigns/<cid>")
def get_campaign_detail(cid):
    c = get_campaign(cid)
    if not c:
        return jsonify({"error": "Not found"}), 404
    leads = get_campaign_leads(cid)
    return jsonify({**c, "leads": leads})


@tracking_bp.post("/campaigns/<cid>/leads")
def add_lead(cid):
    data    = request.get_json(force=True)
    contact = (data.get("contact") or "").strip()
    channel = (data.get("channel") or "").strip()
    status  = (data.get("status")  or "").strip()
    if not contact or not channel or not status:
        return jsonify({"error": "contact, channel, status required"}), 400
    lead = log_outreach(
        cid, contact, channel, status,
        email=data.get("email", ""),
        title=data.get("title", ""),
        notes=data.get("notes", ""),
    )
    return jsonify(lead), 201


@tracking_bp.patch("/leads/<lid>")
def patch_lead(lid):
    data   = request.get_json(force=True)
    status = (data.get("status") or "").strip()
    if not status:
        return jsonify({"error": "status required"}), 400
    lead = update_lead(lid, status, data.get("notes", ""))
    if not lead:
        return jsonify({"error": "Lead not found"}), 404
    return jsonify(lead)


@tracking_bp.get("/campaigns/<cid>/stats")
def get_stats(cid):
    stats = campaign_stats(cid)
    if not stats:
        return jsonify({"error": "Campaign not found"}), 404
    return jsonify(stats)
