from flask import Blueprint, jsonify

from ...core.database import db_manager
from ...services import PassageService

bp = Blueprint("passage", __name__, url_prefix="/api/passage")
passage_service = PassageService()


@bp.route("/<passage_id>", methods=["GET"])
def get_passage(passage_id: str):
    session = db_manager.get_session()
    try:
        passage = passage_service.get_by_id(passage_id, session=session)
        if not passage:
            return jsonify({"error": "Passage not found"}), 404
        payload = passage.to_dict()
        return jsonify(payload)
    finally:
        session.close()
