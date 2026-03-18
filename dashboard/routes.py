import json
<<<<<<< HEAD
from flask import Blueprint, jsonify, render_template
from storage.repo import (
    get_recent_alerts, get_recent_events,
    get_top_suspicious_domains, get_top_suspicious_ips,
    get_query_rate_timeline,
=======
from flask import Blueprint, jsonify, render_template, request
from storage.repo import (
    get_recent_alerts, get_recent_events,
    get_top_suspicious_domains, get_top_suspicious_ips,
    get_query_rate_timeline, get_stats_summary, get_qtype_distribution,
    search_events, clear_alerts,
>>>>>>> 05ab3fa (updated API logic)
)

bp = Blueprint("api", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/api/alerts")
def api_alerts():
<<<<<<< HEAD
    data = get_recent_alerts(50)
=======
    limit = int(request.args.get("limit", 50))
    data = get_recent_alerts(limit)
>>>>>>> 05ab3fa (updated API logic)
    for row in data:
        if isinstance(row.get("reasons"), str):
            try:
                row["reasons"] = json.loads(row["reasons"])
            except Exception:
                row["reasons"] = [row["reasons"]]
    return jsonify(data)

@bp.route("/api/events")
def api_events():
<<<<<<< HEAD
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
=======
    limit = int(request.args.get("limit", 100))
    return jsonify(get_recent_events(limit))

@bp.route("/api/top-domains")
def api_top_domains():
    limit = int(request.args.get("limit", 10))
    return jsonify(get_top_suspicious_domains(limit))

@bp.route("/api/top-ips")
def api_top_ips():
    limit = int(request.args.get("limit", 10))
    return jsonify(get_top_suspicious_ips(limit))

@bp.route("/api/timeline")
def api_timeline():
    minutes = int(request.args.get("minutes", 10))
    return jsonify(get_query_rate_timeline(minutes))

@bp.route("/api/stats")
def api_stats():
    return jsonify(get_stats_summary())

@bp.route("/api/qtype-distribution")
def api_qtype_distribution():
    return jsonify(get_qtype_distribution())

@bp.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    min_score = int(request.args.get("min_score", 0))
    limit = int(request.args.get("limit", 50))
    if not q and min_score == 0:
        return jsonify([])
    return jsonify(search_events(q, min_score, limit))

@bp.route("/api/alerts/clear", methods=["POST"])
def api_clear_alerts():
    count = clear_alerts()
    return jsonify({"cleared": count, "ok": True})
>>>>>>> 05ab3fa (updated API logic)

def register_routes(app):
    app.register_blueprint(bp)
