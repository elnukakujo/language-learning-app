from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import CharacterService
from ...schemas.element_dict import CharacterDict

bp = Blueprint('character', __name__, url_prefix='/api/character')
character_service = CharacterService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_character_from_language(language_id: str):
    """Get all character for a specific language."""
    character = character_service.get_all(language_id = language_id)
    return jsonify([character.to_dict(include_relationships=False) for character in character])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_character_from_unit(unit_id: str):
    """Get all character for a specific unit."""
    character = character_service.get_all(unit_id = unit_id)
    return jsonify([character.to_dict(include_relationships=False) for character in character])


@bp.route('/<character_id>', methods=['GET'])
def get_character(character_id: str):
    """Get a specific character by ID."""
    character = character_service.get_by_id(character_id)
    
    if not character:
        return jsonify({'error': 'character not found'}), 404
    
    return jsonify(character.to_dict(include_relationships=True))


@bp.route('/', methods=['POST'])
def create_character():
    """Create a new character."""
    try:
        # Validate request data
        data = CharacterDict(**request.json)
        
        # Create character
        character = character_service.create(data)
        
        if character:
            return jsonify({
                'success': True,
                'character': character.to_dict(include_relationships=False)
            }), 201
        else:
            return jsonify({'error': 'Failed to create character'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<character_id>', methods=['PUT', 'PATCH'])
def update_character(character_id: str):
    """Update a character."""
    try:
        data = CharacterDict(**request.json)
        
        character = character_service.update(character_id, data)
        
        if character:
            return jsonify({
                'success': True,
                'character': character.to_dict(include_relationships=True)
            })
        else:
            return jsonify({'error': 'character not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<character_id>', methods=['DELETE'])
def delete_character(character_id: str):
    """Delete a character."""
    success = character_service.delete(character_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'character not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_character():
    """Score a character."""
    data = request.json
    character_id = data['character_id']
    success = data['success'].lower() == "true"

    character = character_service.update_score(character_id, success)
    
    if character:
        return jsonify({
            'success': True,
            'character': character.to_dict(include_relationships=False)
        })
    else:
        return jsonify({'error': 'character not found'}), 404