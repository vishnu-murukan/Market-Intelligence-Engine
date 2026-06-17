from flask import Blueprint, request, jsonify
from services.gemini import run_section

outreach_bp = Blueprint("outreach", __name__)


@outreach_bp.post("/generate")
def generate_outreach():
    data    = request.get_json(force=True)
    company  = (data.get("company")  or "").strip()
    category = (data.get("category") or "").strip()
    agency   = (data.get("agency")   or "").strip()
    api_key  = (data.get("apiKey")   or "").strip()
    tone     = (data.get("tone")     or "professional and warm").strip()

    if not company or not category:
        return jsonify({"error": "company and category required"}), 400
    try:
        ctx = f"{agency or 'marketing/branding agency'}. Tone: {tone}."
        result = run_section("outreach", company, category, ctx, api_key)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@outreach_bp.post("/personalize")
def personalize_outreach():
    data         = request.get_json(force=True)
    company      = (data.get("company")      or "").strip()
    category     = (data.get("category")     or "").strip()
    agency       = (data.get("agency")       or "").strip()
    contact_name = (data.get("contactName")  or "").strip()
    contact_role = (data.get("contactRole")  or "marketing leader").strip()
    api_key      = (data.get("apiKey")       or "").strip()

    if not company or not category or not contact_name:
        return jsonify({"error": "company, category, contactName required"}), 400
    try:
        ctx = (f"{agency or 'marketing/branding agency'}. "
               f"This outreach is specifically for {contact_name}, "
               f"{contact_role} at {company}. "
               "Tailor all messaging directly to their role and likely priorities.")
        result = run_section("outreach", company, category, ctx, api_key)
        return jsonify({"result": result, "contact": {"name": contact_name, "role": contact_role}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
