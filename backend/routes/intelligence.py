from flask import Blueprint, request, jsonify, Response, current_app
from services.gemini import stream_all_sections, run_section, SECTION_ORDER
from services.store import create_session, get_session, update_session, list_sessions

intelligence_bp = Blueprint("intelligence", __name__)


@intelligence_bp.get("/sessions")
def get_sessions():
    return jsonify(list_sessions())


@intelligence_bp.get("/sessions/<sid>")
def get_session_route(sid):
    s = get_session(sid)
    if not s:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(s)


@intelligence_bp.post("/run")
def run_research():
    data = request.get_json(force=True)
    company  = (data.get("company")  or "").strip()
    category = (data.get("category") or "").strip()
    agency   = (data.get("agency")   or "").strip()
    api_key  = (data.get("apiKey")   or "").strip()

    if not company or not category:
        return jsonify({"error": "company and category are required"}), 400
    if not api_key and not current_app.config.get("GEMINI_API_KEY"):
        return jsonify({"error": "Gemini API key is required"}), 400

    session_id = create_session(company, category, agency)

    def generate():
        import json
        yield f"event: session\ndata: {json.dumps({'sessionId': session_id})}\n\n"
        yield f"event: start\ndata: {json.dumps({'company': company, 'category': category, 'total': len(SECTION_ORDER)})}\n\n"

        for idx, section_id in enumerate(SECTION_ORDER):
            yield f"event: section_start\ndata: {json.dumps({'sectionId': section_id, 'index': idx})}\n\n"
            try:
                result = run_section(section_id, company, category, agency, api_key)
                update_session(session_id, section_id, result, "done")
                yield f"event: section_done\ndata: {json.dumps({'sectionId': section_id, 'result': result, 'index': idx+1, 'total': len(SECTION_ORDER)})}\n\n"
            except Exception as e:
                update_session(session_id, section_id, f"Error: {e}", "error")
                yield f"event: section_error\ndata: {json.dumps({'sectionId': section_id, 'error': str(e), 'index': idx+1, 'total': len(SECTION_ORDER)})}\n\n"

        import json as _json
        yield f"event: complete\ndata: {_json.dumps({'sessionId': session_id, 'total': len(SECTION_ORDER)})}\n\n"

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@intelligence_bp.post("/run_industry")
def run_industry_research():
    data = request.get_json(force=True)
    industry  = (data.get("industry")  or "").strip()
    agency    = (data.get("agency")    or "").strip()
    api_key   = (data.get("apiKey")    or "").strip()
    force_dem = bool(data.get("demoMode", False))

    if not industry:
        return jsonify({"error": "industry is required"}), 400

    from services.industry_orchestrator import IndustryOrchestrator

    return Response(
        IndustryOrchestrator.stream_pipeline(industry, agency, api_key, force_demo=force_dem),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


@intelligence_bp.post("/section")
def run_single_section():
    data = request.get_json(force=True)
    company    = (data.get("company")   or "").strip()
    category   = (data.get("category")  or "").strip()
    agency     = (data.get("agency")    or "").strip()
    api_key    = (data.get("apiKey")    or "").strip()
    section_id = (data.get("sectionId") or "").strip()

    if not company or not category or not section_id:
        return jsonify({"error": "company, category, sectionId required"}), 400
    try:
        result = run_section(section_id, company, category, agency, api_key)
        return jsonify({"sectionId": section_id, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

