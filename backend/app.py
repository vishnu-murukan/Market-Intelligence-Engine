"""
Market Intelligence Engine — Python/Flask Backend
"""
from flask import Flask
from flask_cors import CORS
from routes.intelligence import intelligence_bp
from routes.outreach import outreach_bp
from routes.tracking import tracking_bp
import os

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

    app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "mie-dev-secret-2025")

    app.register_blueprint(intelligence_bp, url_prefix="/api/intelligence")
    app.register_blueprint(outreach_bp,    url_prefix="/api/outreach")
    app.register_blueprint(tracking_bp,    url_prefix="/api/tracking")

    @app.route("/api/health")
    def health():
        from flask import jsonify
        return jsonify({"status": "ok", "version": "1.0.0"})

    @app.errorhandler(404)
    def not_found(e):
        from flask import jsonify
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import jsonify
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    print("\n* MIE Backend running on http://localhost:4000\n")
    app.run(host="0.0.0.0", port=4000, debug=True)
