from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import VocabularyService
from ...schemas.element_dict import VocabularyDict

bp = Blueprint('vocabulary', __name__, url_prefix='/api/vocabulary')
vocabulary_service = VocabularyService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_vocabulary_from_language(language_id: str):
    """Get all vocabulary for a specific language."""
    vocabulary = vocabulary_service.get_all(language_id = language_id)
    return jsonify([vocab.to_dict() for vocab in vocabulary])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_vocabulary_from_unit(unit_id: str):
    """Get all vocabulary for a specific unit."""
    vocabulary = vocabulary_service.get_all(unit_id = unit_id)
    return jsonify([vocab.to_dict() for vocab in vocabulary])


@bp.route('/<vocabulary_id>', methods=['GET'])
def get_vocabulary(vocabulary_id: str):
    """Get a specific vocabulary by ID."""
    vocabulary = vocabulary_service.get_by_id(vocabulary_id)
    
    if not vocabulary:
        return jsonify({'error': 'Vocabulary not found'}), 404
    
    return jsonify(vocabulary.to_dict())


@bp.route('/', methods=['POST'])
def create_vocabulary():
    """Create a new vocabulary."""
    try:
        # Validate request data
        data = VocabularyDict(**request.json)
        
        # Create vocabulary
        vocabulary = vocabulary_service.create(data)
        
        if vocabulary:
            return jsonify({
                'success': True,
                'vocabulary': vocabulary.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create vocabulary'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<vocabulary_id>', methods=['PUT', 'PATCH'])
def update_vocabulary(vocabulary_id: str):
    """Update a vocabulary."""
    try:
        data = VocabularyDict(**request.json)
        
        vocabulary = vocabulary_service.update(vocabulary_id, data)
        
        if vocabulary:
            return jsonify({
                'success': True,
                'vocabulary': vocabulary.to_dict()
            })
        else:
            return jsonify({'error': 'Vocabulary not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<vocabulary_id>', methods=['DELETE'])
def delete_vocabulary(vocabulary_id: str):
    """Delete a vocabulary."""
    success = vocabulary_service.delete(vocabulary_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'Vocabulary not found'}), 404
    
@bp.route('/score/', methods=['POST'])
def score_vocabulary():
    """Score a vocabulary."""
    data = request.json
    vocabulary_id = data['vocabulary_id']
    success = data['success'].lower() == "true"

    vocabulary = vocabulary_service.update_score(vocabulary_id, success)
    
    if vocabulary:
        return jsonify({
            'success': True,
            'vocabulary': vocabulary.to_dict()
        })
    else:
        return jsonify({'error': 'Vocabulary not found'}), 404