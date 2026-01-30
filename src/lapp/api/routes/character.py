from xml.etree.ElementInclude import include
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import CharacterService
from ...schemas.element_dict import CharacterDict

bp = Blueprint('character', __name__, url_prefix='/api/character')
character_service = CharacterService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_character_from_language(language_id: str):
    """Get all character for a specific language.
    ---
    tags:
        - Character
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve character from
          example: "lang_L1"
    responses:
        200:
            description: List of character
            schema:
                type: array
                items:
                    type: object
                    description: Character object
    """
    character = character_service.get_all(language_id = language_id)
    return jsonify([character.to_dict() for character in character])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_character_from_unit(unit_id: str):
    """Get all character for a specific unit.
    ---
    tags:
        - Character
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve character from
          example: "unit_U1"
    responses:
        200:
            description: List of character
            schema:
                type: array
                items:
                    type: object
                    description: Character object    
    """
    character = character_service.get_all(unit_id = unit_id)
    return jsonify([character.to_dict() for character in character])


@bp.route('/<character_id>', methods=['GET'])
def get_character(character_id: str):
    """Get a specific character by ID.
    ---
    tags:
        - Character
    parameters:
        - name: character_id
          in: path
          type: string
          required: true
          description: The ID of the character to retrieve
          example: "char_C1"
    responses:
        200:
            description: Character object
            schema:
                type: object
                description: Character object
    """
    character = character_service.get_by_id(character_id)
    
    if not character:
        return jsonify({'error': 'character not found'}), 404
    
    return jsonify(character.to_dict())


@bp.route('/', methods=['POST'])
def create_character():
    """Create a new character.
    ---
    tags:
        - Character
    parameters:
        - name: character
          in: body
          required: true
          description: The character to create
          schema:
              type: object
              properties:
                  unit_id:
                      type: string
                      example: "unit_U1"
                      description: The ID of the unit the character belongs to
                      required: true
                  character:
                      type: string
                      example: "漢"
                      description: The character itself
                      required: true
                  components:
                      type: string
                      example: "氵, 艹"
                      description: Components of the character
                      required: false
                  phonetic:
                      type: string
                      example: "hàn"
                      description: The phonetic representation of the character
                      required: true
                  meaning:
                      type: string
                      example: "Chinese"
                      description: The meaning of the character
                      required: true
                  example_word:
                      type: string
                      example: "漢字"
                      description: Example word using the character
                      required: false
                  image_files:
                      type: array
                      items:
                        type: string
                        example: "/path/to/image1.jpg"
                        required: false
                        description: List of image file paths
                  audio_files:
                      type: array
                      items:
                        type: string
                        example: "/path/to/audio1.mp3"
                        required: false
                        description: List of audio file paths
    responses:
        201:
            description: Character created successfully
            schema:
                type: object
                description: The created character object
        400:
            description: Character creation failed
    """
    try:
        # Validate request data
        data = CharacterDict(**request.json)
        
        # Create character
        character = character_service.create(data)
        
        if character:
            return jsonify({
                'success': True,
                'character': character.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create character'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<character_id>', methods=['PUT', 'PATCH'])
def update_character(character_id: str):
    """Update a character.
    ---
    tags:
        - Character
    parameters:
        - name: character_id
          in: path
          type: string
          required: true
          description: The ID of the character to update
          example: "char_C1"
        - name: body
          in: body
          required: true
          schema:
              type: object
              properties:
                  unit_id:
                      type: string
                      example: "unit_U1"
                      required: true
                  character:
                      type: string
                      example: "漢"
                      required: true
                  components:
                      type: string
                      example: "氵, 艹"
                      required: false
                  phonetic:
                      type: string
                      example: "hàn"
                      required: true
                  meaning:
                      type: string
                      example: "Chinese"
                      required: true
                  example_word:
                      type: string
                      example: "漢字"
                      required: false
                  image_files:
                      type: array
                      items:
                        type: string
                        example: "/path/to/image1.jpg"
                        required: false
                        description: List of image file paths
                  audio_files:
                      type: array
                      items:
                        type: string
                        example: "/path/to/audio1.mp3"
                        required: false
                        description: List of audio file paths
    responses:
        201:
            description: Character updated successfully
            schema:
                type: object
                description: The updated character object
        400:
            description: Character update failed
    """
    try:
        data = CharacterDict(**request.json)
        
        character = character_service.update(character_id, data)
        
        if character:
            return jsonify({
                'success': True,
                'character': character.to_dict()
            }), 201
        else:
            return jsonify({'error': 'character not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<character_id>', methods=['DELETE'])
def delete_character(character_id: str):
    """Delete a character.
    ---
    tags:
        - Character
    parameters:
        - name: character_id
          in: path
          type: string
          required: true
          description: The ID of the character to delete
          example: "char_C1"
    responses:
        204:
            description: Character deleted successfully
        404:
            description: Character not found
    """
    success = character_service.delete(character_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'character not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_character():
    """Score a character.
    ---
    tags:
        - Character
    parameters:
        - name: body
          in: body
          required: true
          schema:
              type: object
              properties:
                  character_id:
                      type: string
                      example: "char_C1"
                      description: The ID of the character to score
                      required: true
                  success:
                      type: string
                      example: "true"
                      description: Whether the scoring was successful
                      required: true
    responses:
        200:
            description: Character scored successfully
            schema:
                type: object
                description: The scored character object
        404:
            description: character not found
    """
    data = request.json
    character_id = data['character_id']
    success = data['success'].lower() == "true"

    character = character_service.update_score(character_id, success)
    
    if character:
        return jsonify({
            'success': True,
            'character': character.to_dict(include_relations=False)
        })
    else:
        return jsonify({'error': 'character not found'}), 404