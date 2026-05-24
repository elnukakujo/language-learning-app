from flask import Blueprint, jsonify

from ...core.database import db_manager
from ...services import WordService

bp = Blueprint("word", __name__, url_prefix="/api/word")
word_service = WordService()


@bp.route("/<word_id>", methods=["GET"])
def get_word(word_id: str):
    session = db_manager.get_session()
    try:
        word = word_service.get_by_id(word_id, session=session)
        if not word:
            return jsonify({"error": "Word not found"}), 404
        payload = word.to_dict()
        return jsonify(payload)
    finally:
        session.close()
