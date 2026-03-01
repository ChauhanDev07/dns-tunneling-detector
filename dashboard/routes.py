import json
from flask import Blueprint, jsonify, render_template
from storage.repo import (
    get_recent_alerts, get_recent_events,
    get_top_suspicious_domains, get_top_suspicious_ips,
    get_query_rate_timeline,
)

bp = Blueprint("api", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/api/alerts")
def api_alerts():
    data = get_recent_alerts(50)
    for row in data:
        if isinstance(row.get("reasons"), str):
            try:
                row["reasons"] = json.loads(row["reasons"])
            except Exception:
                row["reasons"] = [row["reasons"]]
    return jsonify(data)

@bp.route("/api/events")
def api_events():
    return jsonify(get_recent_events(100))

@bp.route("/api/top-domains")
def api_top_domains():
    return jsonify(get_top_suspicious_domains(10))

@bp.route("/api/top-ips")
def api_top_ips():
    return jsonify(get_top_suspicious_ips(10))

@bp.route("/api/timeline")
def api_timeline():
    return jsonify(get_query_rate_timeline(10))

def register_routes(app):
    app.register_blueprint(bp)
