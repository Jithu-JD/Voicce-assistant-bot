# app/__init__.py
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from .config import Settings
import uuid

# timing helpers (we'll create app/utils/timing.py next)
from .utils.timing import start_trace

settings = Settings()  # loads env

def create_app():
    app = Flask(__name__)
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    CORS(app, resources={r"/api/*": {"origins": settings.CORS_ORIGINS}})

    # ---- timing hooks (prints one summary line per request) ----
    @app.before_request
    def _trace_start():
        rid = request.headers.get("X-Request-Id") or str(uuid.uuid4())[:8]
        g.rid = rid
        g.trace, g.trace_log = start_trace(f"{request.method} {request.path} rid={rid}")

    @app.after_request
    def _trace_end(resp):
        try:
            # one compact line like:
            # [TRACE] POST /api/conversation/chat rid=abcd1234 :: openai.chat [...]: 812ms | lm.pass2: 640ms || total: 1530ms
            g.trace_log()
        except Exception:
            pass
        return resp

    # ---- blueprints ----
    from .routes.auth import bp as auth_bp
    from .routes.conversation import bp as convo_bp
    from .routes.speech import bp as speech_bp
    from .routes.knowledge import bp as kb_bp
    from .routes.analytics import bp as analytics_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(convo_bp, url_prefix="/api/conversation")
    app.register_blueprint(speech_bp, url_prefix="/api/speech")
    app.register_blueprint(kb_bp, url_prefix="/api/knowledge")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    # simple health/ping
    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "service": "aira-backend"})

    @app.errorhandler(Exception)
    def handle_error(e):
        return jsonify({"ok": False, "error": str(e)}), 500

    return app
