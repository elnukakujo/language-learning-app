from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import LanguageService
from ...schemas.element_dict import LanguageDict

bp = Blueprint('language', __name__, url_prefix='/api/languages')
language_service = LanguageService()

@bp.route('/', methods=['GET'])
def get_all_languages():
    """Get all languages."""
    languages = language_service.get_all()
    return jsonify([lang.to_dict() for lang in languages])


@bp.route('/<language_id>', methods=['GET'])
def get_language(language_id: str):
    """Get a specific language by ID."""
    language = language_service.get_by_id(language_id)
    
    if not language:
        return jsonify({'error': 'Language not found'}), 404
    
    return jsonify(language.to_dict(include_relationships=False))


@bp.route('/', methods=['POST'])
def create_language():
    """Create a new language."""
    try:
        # Validate request data
        data = LanguageDict(**request.json)
        
        # Create language
        language = language_service.create(data)
        
        if language:
            return jsonify({
                'success': True,
                'language': language.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create language'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<language_id>', methods=['PUT', 'PATCH'])
def update_language(language_id: str):
    """Update a language."""
    try:
        data = LanguageDict(**request.json)
        
        language = language_service.update(language_id, data)
        
        if language:
            return jsonify({
                'success': True,
                'language': language.to_dict()
            })
        else:
            return jsonify({'error': 'Language not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<language_id>', methods=['DELETE'])
def delete_language(language_id: str):
    """Delete a language."""
    success = language_service.delete(language_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'Language not found'}), 404