from xml.etree.ElementInclude import include
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import CalligraphyService
from ...schemas.features import CalligraphyDict

bp = Blueprint('calligraphy', __name__, url_prefix='/api/calligraphy')
calligraphy_service = CalligraphyService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_calligraphy_from_language(language_id: str):
    """Get all calligraphy for a specific language.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve calligraphy from
          example: "lang_L1"
    responses:
        200:
            description: List of calligraphy
            schema:
                type: array
                items:
                    type: object
                    description: calligraphy object
    """
    calligraphy = calligraphy_service.get_all(language_id = language_id)
    return jsonify([calligraphy.to_dict() for calligraphy in calligraphy])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_calligraphy_from_unit(unit_id: str):
    """Get all calligraphy for a specific unit.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve calligraphy from
          example: "unit_U1"
    responses:
        200:
            description: List of calligraphy
            schema:
                type: array
                items:
                    type: object
                    description: calligraphy object    
    """
    calligraphy = calligraphy_service.get_all(unit_id = unit_id)
    return jsonify([calligraphy.to_dict() for calligraphy in calligraphy])


@bp.route('/<calligraphy_id>', methods=['GET'])
def get_calligraphy(calligraphy_id: str):
    """Get a specific calligraphy by ID.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: calligraphy_id
          in: path
          type: string
          required: true
          description: The ID of the calligraphy to retrieve
          example: "char_C1"
    responses:
        200:
            description: calligraphy object
            schema:
                type: object
                description: calligraphy object
    """
    calligraphy = calligraphy_service.get_by_id(calligraphy_id)
    
    if not calligraphy:
        return jsonify({'error': 'calligraphy not found'}), 404
    
    return jsonify(calligraphy.to_dict())


@bp.route('/', methods=['POST'])
def create_calligraphy():
    """Create a new calligraphy.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: calligraphy
          in: body
          required: true
          description: The calligraphy to create
          schema:
              type: object
              properties:
                  unit_id:
                      type: string
                      example: "unit_U1"
                      description: The ID of the unit the calligraphy belongs to
                      required: true
                  calligraphy:
                      type: string
                      example: "漢"
                      description: The calligraphy itself
                      required: true
                  components:
                      type: string
                      example: "氵, 艹"
                      description: Components of the calligraphy
                      required: false
                  phonetic:
                      type: string
                      example: "hàn"
                      description: The phonetic representation of the calligraphy
                      required: true
                  meaning:
                      type: string
                      example: "Chinese"
                      description: The meaning of the calligraphy
                      required: true
                  example_word:
                      type: string
                      example: "漢字"
                      description: Example word using the calligraphy
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
            description: calligraphy created successfully
            schema:
                type: object
                description: The created calligraphy object
        400:
            description: calligraphy creation failed
    """
    try:
        # Validate request data
        data = CalligraphyDict(**request.json)
        
        # Create calligraphy
        calligraphy = calligraphy_service.create(data)
        
        if calligraphy:
            return jsonify({
                'success': True,
                'calligraphy': calligraphy.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create calligraphy'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<calligraphy_id>', methods=['PUT', 'PATCH'])
def update_calligraphy(calligraphy_id: str):
    """Update a calligraphy.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: calligraphy_id
          in: path
          type: string
          required: true
          description: The ID of the calligraphy to update
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
                  calligraphy:
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
            description: calligraphy updated successfully
            schema:
                type: object
                description: The updated calligraphy object
        400:
            description: calligraphy update failed
    """
    try:
        data = CalligraphyDict(**request.json)
        
        calligraphy = calligraphy_service.update(calligraphy_id, data)
        
        if calligraphy:
            return jsonify({
                'success': True,
                'calligraphy': calligraphy.to_dict()
            }), 201
        else:
            return jsonify({'error': 'calligraphy not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<calligraphy_id>', methods=['DELETE'])
def delete_calligraphy(calligraphy_id: str):
    """Delete a calligraphy.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: calligraphy_id
          in: path
          type: string
          required: true
          description: The ID of the calligraphy to delete
          example: "char_C1"
    responses:
        204:
            description: calligraphy deleted successfully
        404:
            description: calligraphy not found
    """
    success = calligraphy_service.delete(calligraphy_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'calligraphy not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_calligraphy():
    """Score a calligraphy.
    ---
    tags:
        - Calligraphy
    parameters:
        - name: body
          in: body
          required: true
          schema:
              type: object
              properties:
                  calligraphy_id:
                      type: string
                      example: "char_C1"
                      description: The ID of the calligraphy to score
                      required: true
                  success:
                      type: string
                      example: "true"
                      description: Whether the scoring was successful
                      required: true
    responses:
        200:
            description: calligraphy scored successfully
            schema:
                type: object
                description: The scored calligraphy object
        404:
            description: calligraphy not found
    """
    data = request.json
    calligraphy_id = data['calligraphy_id']
    success = data['success'].lower() == "true"

    calligraphy = calligraphy_service.update_score(calligraphy_id, success)
    
    if calligraphy:
        return jsonify({
            'success': True,
            'calligraphy': calligraphy.to_dict(include_relations=False)
        })
    else:
        return jsonify({'error': 'calligraphy not found'}), 404