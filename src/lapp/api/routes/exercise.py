from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import ExerciseService
from ...schemas.element_dict import ExerciseDict

bp = Blueprint('exercise', __name__, url_prefix='/api/exercise')
exercise_service = ExerciseService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_exercise_from_language(language_id: str):
    """Get all exercise for a specific language."""
    exercise = exercise_service.get_all(language_id = language_id)
    return jsonify([exercise.to_dict() for exercise in exercise])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_exercise_from_unit(unit_id: str):
    """Get all exercise for a specific unit."""
    exercise = exercise_service.get_all(unit_id = unit_id)
    return jsonify([exercise.to_dict() for exercise in exercise])


@bp.route('/<exercise_id>', methods=['GET'])
def get_exercise(exercise_id: str):
    """Get a specific exercise by ID."""
    exercise = exercise_service.get_by_id(exercise_id)
    
    if not exercise:
        return jsonify({'error': 'exercise not found'}), 404
    
    return jsonify(exercise.to_dict())


@bp.route('/', methods=['POST'])
def create_exercise():
    """Create a new exercise."""
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
    """Update a exercise."""
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
    """Delete a exercise."""
    success = exercise_service.delete(exercise_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'exercise not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_exercise():
    """Score a exercise."""
    data = request.json
    exercise_id = data['exercise_id']
    success = data['success'].lower() == "true"

    exercise = exercise_service.update_score(exercise_id, success)
    
    if exercise:
        return jsonify({
            'success': True,
            'exercise': exercise.to_dict()
        })
    else:
        return jsonify({'error': 'exercise not found'}), 404