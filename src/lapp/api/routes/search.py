from flask import Blueprint, jsonify, request

from ...services import SearchService

bp = Blueprint("search", __name__, url_prefix="/api/search")
search_service = SearchService()


@bp.route("", methods=["GET"])
def search_elements():
    query = (request.args.get("q") or "").strip()
    if len(query) < 1:
        return jsonify({"error": "Query must be at least 1 character long"}), 400

    user_id = request.headers.get("X-User-Id") or request.cookies.get("selected_user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    results = search_service.search_elements(user_id=user_id, query=query)
    return jsonify({"results": results}), 200
