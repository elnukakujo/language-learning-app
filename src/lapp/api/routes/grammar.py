from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import GrammarService
from ...schemas import GrammarDict

bp = Blueprint('grammar', __name__, url_prefix='/api/grammar')
grammar_service = GrammarService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_grammar_from_language(language_id: str):
    """Get all grammar for a specific language.
    --- 
    tags:
        - Grammar
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve grammar for
          example: "lang_L1"
    responses:
        200:
            description: A list of grammar items
            schema:
                type: array
                items:
                    type: object
                    description: "A Grammar object"
    """
    grammar = grammar_service.get_all(language_id = language_id)
    return jsonify([grammar.to_dict() for grammar in grammar])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_grammar_from_unit(unit_id: str):
    """Get all grammar for a specific unit.
    --- 
    tags:
        - Grammar
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve grammar for
          example: "unit_U1"
    responses:
        200:
            description: A list of grammar items
            schema:
                type: array
                items:
                    type: object
                    description: "A Grammar object"
    """
    grammar = grammar_service.get_all(unit_id = unit_id)
    return jsonify([grammar.to_dict() for grammar in grammar])


@bp.route('/<grammar_id>', methods=['GET'])
def get_grammar(grammar_id: str):
    """Get a specific grammar by ID.
    ---
    tags:
        - Grammar
    parameters:
        - name: grammar_id
          in: path
          type: string
          required: true
          description: The ID of the grammar to retrieve
          example: "gram_G1"
    responses:
        200:
            description: A Grammar object
            schema:
                type: object
        404:
            description: Grammar not found
    """
    grammar = grammar_service.get_by_id(grammar_id)
    
    if not grammar:
        return jsonify({'error': 'grammar not found'}), 404
    
    return jsonify(grammar.to_dict()), 200


@bp.route('/', methods=['POST'])
def create_grammar():
    """Create a new grammar.
    ---
    tags:
        - Grammar
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Grammar data
            properties:
                title:
                    type: string
                    example: "Past Tense"
                    required: true
                    description: "Title of the grammar"
                explanation:
                    type: string
                    example: "The past tense is used to describe actions that have already happened."
                    required: true
                    description: "Explanation of the grammar"
                learnable_sentence:
                    type: string
                    example: "I walked to the store yesterday."
                    required: false
                    description: "A sentence that illustrates the grammar point"
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
            description: Grammar created successfully
            schema:
                type: object
        400:
            description: Validation error or failed to create grammar
    """
    try:
        # Validate request data
        data = GrammarDict(**request.json)
        
        # Create grammar
        grammar = grammar_service.create(data)
        
        if grammar:
            return jsonify({
                'success': True,
                'grammar': grammar.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create grammar'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<grammar_id>', methods=['PUT', 'PATCH'])
def update_grammar(grammar_id: str):
    """Update a grammar.
    ---
    tags:
        - Grammar
    parameters:
        - name: grammar_id
          in: path
          type: string
          required: true
          description: The ID of the grammar to update
          example: "gram_G1"
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Grammar data
            properties:
                title:
                    type: string
                    example: "Past Tense"
                    required: true
                    description: "Title of the grammar"
                explanation:
                    type: string
                    example: "The past tense is used to describe actions that have already happened."
                    required: true
                    description: "Explanation of the grammar"
                learnable_sentence:
                    type: string
                    example: "I walked to the store yesterday."
                    required: false
                    description: "A sentence that illustrates the grammar point"
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
            description: Grammar created successfully
            schema:
                type: object
        404:
            description: grammar not found
        400:
            description: Validation error
    """
    try:
        data = GrammarDict(**request.json)
        
        grammar = grammar_service.update(grammar_id, data)
        
        if grammar:
            return jsonify({
                'success': True,
                'grammar': grammar.to_dict()
            })
        else:
            return jsonify({'error': 'grammar not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<grammar_id>', methods=['DELETE'])
def delete_grammar(grammar_id: str):
    """Delete a grammar.
    ---
    tags:
        - Grammar
    parameters:
        - name: grammar_id
          in: path
          type: string
          required: true
          description: The ID of the grammar to delete
          example: "gram_G1"
    responses:
        204:
            description: Grammar deleted successfully
        404:
            description: grammar not found
    """
    success = grammar_service.delete(grammar_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'grammar not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_grammar():
    """Score a grammar.
    ---
    tags:
        - Grammar
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Score data
            properties:
                grammar_id:
                    type: string
                    example: "gram_G1"
                    required: true
                    description: "The ID of the grammar to score"
                success:
                    type: boolean
                    example: "true"
                    required: true
                    description: "Whether the user answered correctly"
    responses:
        200:
            description: Grammar scored successfully
    """
    data = request.json
    grammar_id = data['grammar_id']
    success = data['success'].lower() == "true"

    grammar = grammar_service.update_score(grammar_id, success)
    
    if grammar:
        return jsonify({
            'success': True,
            'grammar': grammar.to_dict(include_relations=False)
        })
    else:
        return jsonify({'error': 'grammar not found'}), 404