from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import VocabularyService
from ...schemas.features import VocabularyDict

bp = Blueprint('vocabulary', __name__, url_prefix='/api/vocabulary')
vocabulary_service = VocabularyService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_vocabulary_from_language(language_id: str):
    """Get all vocabulary for a specific language.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve vocabulary from
          example: "lang_L1"
    responses:
        200:
            description: List of vocabulary
            schema:
                type: array
                items:
                    type: object
                    description: Vocabulary object
    """
    vocabulary = vocabulary_service.get_all(language_id=language_id, as_dict=True)
    return jsonify(vocabulary)


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_vocabulary_from_unit(unit_id: str):
    """Get all vocabulary for a specific unit.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve vocabulary from
          example: "unit_U1"
    responses:
        200:
            description: List of vocabulary
            schema:
                type: array
                items:
                    type: object
                    description: Vocabulary object
    """
    vocabulary = vocabulary_service.get_all(unit_id=unit_id, as_dict=True)
    return jsonify(vocabulary)


@bp.route('/<vocabulary_id>', methods=['GET'])
def get_vocabulary(vocabulary_id: str):
    """Get a specific vocabulary by ID.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: vocabulary_id
          in: path
          type: string
          required: true
          description: The ID of the vocabulary to retrieve
    responses:
        200:
            description: Vocabulary object
            schema:
                type: object
        404:
            description: Vocabulary not found
    """
    vocabulary = vocabulary_service.get_by_id(vocabulary_id, as_dict=True)
    
    if not vocabulary:
        return jsonify({'error': 'Vocabulary not found'}), 404
    
    return jsonify(vocabulary)


@bp.route('/', methods=['POST'])
def create_vocabulary():
    """Create a new vocabulary.
    ---
    tags:
        - Vocabulary
    parameters:
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
                  word:
                      type: object
                      properties:
                          word:
                              type: string
                              example: "Bonjour"
                              required: true
                          translation:
                              type: string
                              example: "Hello"
                              required: true
                          phonetic:
                              type: string
                              example: "bɔ̃ʒuʁ"
                              required: false
                          type:
                              type: string
                              example: "interjection"
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
                  example_sentences:
                      type: array
                      items:
                          type: object
                          properties:
                              text:
                                  type: string
                                  example: "Bonjour! Comment ça va?"
                                  required: true
                              translation:
                                  type: string
                                  example: "Hello! How are you?"
                                  required: true
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
            description: Vocabulary created successfully
            schema:
                type: object
        400:
            description: Validation error
    """
    try:
        # Validate request data
        data = VocabularyDict(**request.json)
        
        # Create vocabulary
        vocabulary = vocabulary_service.create(data, as_dict=True)
        
        if vocabulary:
            return jsonify({
                'success': True,
                'vocabulary': vocabulary
            }), 201
        else:
            return jsonify({'error': 'Failed to create vocabulary'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<vocabulary_id>', methods=['PUT', 'PATCH'])
def update_vocabulary(vocabulary_id: str):
    """Update a vocabulary.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: vocabulary_id
          in: path
          type: string
          required: true
          description: The ID of the vocabulary to update
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
                  word:
                      type: object
                      properties:
                          word:
                              type: string
                              example: "Bonjour"
                              required: true
                          translation:
                              type: string
                              example: "Hello"
                              required: true
                          phonetic:
                              type: string
                              example: "bɔ̃ʒuʁ"
                              required: false
                          type:
                              type: string
                              example: "interjection"
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
                  example_sentences:
                      type: array
                      items:
                          type: object
                          properties:
                              text:
                                  type: string
                                  example: "Bonjour! Comment ça va?"
                                  required: true
                              translation:
                                  type: string
                                  example: "Hello! How are you?"
                                  required: true
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
        200:
            description: Vocabulary updated successfully
            schema:
                type: object
        400:
            description: Validation error
        404:
            description: Vocabulary not found
    """
    try:
        data = VocabularyDict(**request.json)
        
        vocabulary = vocabulary_service.update(vocabulary_id, data, as_dict=True)
        
        if vocabulary:
            return jsonify({
                'success': True,
                'vocabulary': vocabulary
            })
        else:
            return jsonify({'error': 'Vocabulary not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<vocabulary_id>', methods=['DELETE'])
def delete_vocabulary(vocabulary_id: str):
    """Delete a vocabulary.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: vocabulary_id
          in: path
          type: string
          required: true
          description: The ID of the vocabulary to delete
    responses:
        204:
            description: Vocabulary deleted successfully
        404:
            description: Vocabulary not found    
    """
    success = vocabulary_service.delete(vocabulary_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'Vocabulary not found'}), 404
    
@bp.route('/score/', methods=['POST'])
def score_vocabulary():
    """Score a vocabulary.
    ---
    tags:
        - Vocabulary
    parameters:
        - name: body
          in: body
          required: true
          schema:
              type: object
              properties:
                  vocabulary_id:
                      type: string
                      example: "voc_V1"
                      required: true
                      description: The ID of the vocabulary to score
                  success:
                      type: string
                      example: "true"
                      required: true
                      description: Whether the user answered correctly
    responses:
        200:
            description: Vocabulary scored successfully
            schema:
                type: object
        404:
            description: Vocabulary not found
    """
    data = request.json
    vocabulary_id = data['vocabulary_id']
    success = data['success'].lower() == "true"

    vocabulary = vocabulary_service.update_score(vocabulary_id, success, as_dict=True, include_relations=False)
    
    if vocabulary:
        return jsonify({
            'success': True,
            'vocabulary': vocabulary
        })
    else:
        return jsonify({'error': 'Vocabulary not found'}), 404