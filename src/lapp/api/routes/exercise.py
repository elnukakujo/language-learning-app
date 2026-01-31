from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import ExerciseService
from ...schemas.features import ExerciseDict

bp = Blueprint('exercise', __name__, url_prefix='/api/exercise')
exercise_service = ExerciseService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_exercise_from_language(language_id: str):
    """Get all exercise for a specific language.
    ---
    tags:
        - Exercise
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve exercise from
          example: "lang_L1"
    responses:
        200:
            description: List of exercise
            schema:
                type: array
                items:
                    type: object
                    description: Exercise object
    """
    exercise = exercise_service.get_all(language_id = language_id)
    return jsonify([exercise.to_dict() for exercise in exercise])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_exercise_from_unit(unit_id: str):
    """Get all exercise for a specific unit.
    ---
    tags:
        - Exercise
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve exercise from
          example: "unit_U1"
    responses:
        200:
            description: List of exercise
            schema:
                type: array
                items:
                    type: object
                    description: Exercise object
    """
    exercise = exercise_service.get_all(unit_id = unit_id)
    return jsonify([exercise.to_dict() for exercise in exercise])


@bp.route('/<exercise_id>', methods=['GET'])
def get_exercise(exercise_id: str):
    """Get a specific exercise by ID.
    ---
    tags:
        - Exercise
    parameters:
        - name: exercise_id
          in: path
          type: string
          required: true
          description: The ID of the exercise to retrieve
          example: "ex_E1"
    responses:
        200:
            description: Exercise object
            schema:
                type: object
                description: Exercise object
        404:
            description: Exercise not found
    """
    exercise = exercise_service.get_by_id(exercise_id)
    
    if not exercise:
        return jsonify({'error': 'exercise not found'}), 404
    
    return jsonify(exercise.to_dict())


@bp.route('/', methods=['POST'])
def create_exercise():
    """Create a new exercise.
    ---
    tags:
        - Exercise
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Exercise object
            properties:
                unit_id:
                    type: string
                    example: "unit_U1"
                    description: "ID of the unit this exercise belongs to"
                    required: true
                exercise_type:
                    type: string
                    example: "translate"
                    description: "Type of the exercise, can be essay, answering, translate, organize, fill_in_the_blank, matching, or true_false"
                    required: true
                question:
                    type: string
                    example: "What is the capital of France?"
                    required: true
                    description: "The question or prompt for the exercise"
                text_support:
                    type: string
                    example: "Additional information"
                    description: "Additional text support for the exercise"
                    required: false
                image_files:
                    type: array
                    items:
                        type: string
                    example: ["/path/to/image1.png", "/path/to/image2.png"]
                    description: "List of image file paths associated with the exercise"
                    required: false
                audio_files:
                    type: array
                    items:
                        type: string
                    example: ["/path/to/audio1.mp3"]
                    description: "List of audio file paths associated with the exercise"
                    required: false
                answer:
                    type: string
                    example: "Paris"
                    required: true
                    description: "The correct answer for the exercise"
                vocabulary_ids:
                    type: array
                    items:
                        type: string
                    example: ["voc_V1"]
                    description: "List of associated vocabulary IDs"
                    required: false
                calligraphy_ids:
                    type: array
                    items:
                        type: string
                    example: ["call_C1"]
                    description: "List of associated calligraphy IDs"
                    required: false
                grammar_ids:
                    type: array
                    items:
                        type: string
                    example: ["gram_G1"]
                    description: "List of associated grammar IDs"
                    required: false
    responses:
        201:
            description: Exercise created successfully
            schema:
                type: object
                description: Created Exercise object
        400:
            description: Validation error or bad request
    """
    try:
        # Validate request data
        data = ExerciseDict(**request.json)
        
        # Create exercise
        exercise = exercise_service.create(data)
        
        if exercise:
            return jsonify({
                'success': True,
                'exercise': exercise.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create exercise'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<exercise_id>', methods=['PUT', 'PATCH'])
def update_exercise(exercise_id: str):
    """Update a exercise.
    ---
    tags:
        - Exercise
    parameters:
        - name: exercise_id
          in: path
          type: string
          required: true
          description: The ID of the exercise to update
          example: "ex_E1"
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Exercise object
            properties:
                unit_id:
                    type: string
                    example: "unit_U1"
                    description: "ID of the unit this exercise belongs to"
                    required: true
                exercise_type:
                    type: string
                    example: "translate"
                    description: "Type of the exercise, can be essay, answering, translate, organize, fill_in_the_blank, matching, or true_false"
                    required: true
                question:
                    type: string
                    example: "What is the capital of France?"
                    required: true
                    description: "The question or prompt for the exercise"
                text_support:
                    type: string
                    example: "Additional information"
                    description: "Additional text support for the exercise"
                    required: false
                image_files:
                    type: array
                    items:
                        type: string
                    example: ["/path/to/image1.png", "/path/to/image2.png"]
                    description: "List of image file paths associated with the exercise"
                    required: false
                audio_files:
                    type: array
                    items:
                        type: string
                    example: ["/path/to/audio1.mp3"]
                    description: "List of audio file paths associated with the exercise"
                    required: false
                answer:
                    type: string
                    example: "Paris"
                    required: true
                    description: "The correct answer for the exercise"
                vocabulary_ids:
                    type: array
                    items:
                        type: string
                    example: ["voc_V1"]
                    description: "List of associated vocabulary IDs"
                    required: false
                calligraphy_ids:
                    type: array
                    items:
                        type: string
                    example: ["call_C1"]
                    description: "List of associated calligraphy IDs"
                    required: false
                grammar_ids:
                    type: array
                    items:
                        type: string
                    example: ["gram_G1"]
                    description: "List of associated grammar IDs"
                    required: false
    responses:
        201:
            description: Exercise created successfully
            schema:
                type: object
                description: Created Exercise object
        400:
            description: Validation error or bad request
    """
    try:
        data = ExerciseDict(**request.json)
        
        exercise = exercise_service.update(exercise_id, data)
        
        if exercise:
            return jsonify({
                'success': True,
                'exercise': exercise.to_dict()
            })
        else:
            return jsonify({'error': 'exercise not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id: str):
    """Delete an exercise.
    ---
    tags:
        - Exercise
    parameters:
        - name: exercise_id
          in: path
          type: string
          required: true
          description: The ID of the exercise to delete
          example: "ex_E1"
    responses:
        204:
            description: Exercise deleted successfully
        404:
            description: Exercise not found
    """
    success = exercise_service.delete(exercise_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'exercise not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_exercise():
    """Score an exercise.
    ---
    tags:
        - Exercise
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Score update object
            properties:
                exercise_id:
                    type: string
                    example: "ex_E1"
                    description: "ID of the exercise to score"
                    required: true
                success:
                    type: string
                    example: "true"
                    description: "Whether the exercise was answered correctly ('true' or 'false')"
                    required: true
    responses:
        200:
            description: Exercise scored successfully
            schema:
                type: object
                description: Updated Exercise object
        404:
            description: Exercise not found
    """
    data = request.json
    exercise_id = data['exercise_id']
    success = data['success'].lower() == "true"

    exercise = exercise_service.update_score(exercise_id, success)
    
    if exercise:
        return jsonify({
            'success': True,
            'exercise': exercise.to_dict(include_relations=False)
        })
    else:
        return jsonify({'error': 'exercise not found'}), 404