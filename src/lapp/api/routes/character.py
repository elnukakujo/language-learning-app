from flask import Blueprint, jsonify

from ...core.database import db_manager
from ...services import CharacterService

bp = Blueprint("character", __name__, url_prefix="/api/character")
character_service = CharacterService()


@bp.route("/<character_id>", methods=["GET"])
def get_character(character_id: str):
    session = db_manager.get_session()
    try:
        character = character_service.get_by_id(character_id, session=session)
        if not character:
            return jsonify({"error": "Character not found"}), 404
        payload = character.to_dict()
        return jsonify(payload)
    finally:
        session.close()
