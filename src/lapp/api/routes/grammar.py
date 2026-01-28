from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import GrammarService
from ...schemas.element_dict import GrammarDict

bp = Blueprint('grammar', __name__, url_prefix='/api/grammar')
grammar_service = GrammarService()

@bp.route('/language/<language_id>', methods=['GET'])
def get_all_grammar_from_language(language_id: str):
    """Get all grammar for a specific language."""
    grammar = grammar_service.get_all(language_id = language_id)
    return jsonify([grammar.to_dict(include_relationships=False) for grammar in grammar])


@bp.route('/unit/<unit_id>', methods=['GET'])
def get_all_grammar_from_unit(unit_id: str):
    """Get all grammar for a specific unit."""
    grammar = grammar_service.get_all(unit_id = unit_id)
    return jsonify([grammar.to_dict(include_relationships=False) for grammar in grammar])


@bp.route('/<grammar_id>', methods=['GET'])
def get_grammar(grammar_id: str):
    """Get a specific grammar by ID."""
    grammar = grammar_service.get_by_id(grammar_id)
    
    if not grammar:
        return jsonify({'error': 'grammar not found'}), 404
    
    return jsonify(grammar.to_dict(include_relationships=True))


@bp.route('/', methods=['POST'])
def create_grammar():
    """Create a new grammar."""
    try:
        # Validate request data
        data = GrammarDict(**request.json)
        
        # Create grammar
        grammar = grammar_service.create(data)
        
        if grammar:
            return jsonify({
                'success': True,
                'grammar': grammar.to_dict(include_relationships=True)
            }), 201
        else:
            return jsonify({'error': 'Failed to create grammar'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<grammar_id>', methods=['PUT', 'PATCH'])
def update_grammar(grammar_id: str):
    """Update a grammar."""
    try:
        data = GrammarDict(**request.json)
        
        grammar = grammar_service.update(grammar_id, data)
        
        if grammar:
            return jsonify({
                'success': True,
                'grammar': grammar.to_dict(include_relationships=True)
            })
        else:
            return jsonify({'error': 'grammar not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<grammar_id>', methods=['DELETE'])
def delete_grammar(grammar_id: str):
    """Delete a grammar."""
    success = grammar_service.delete(grammar_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'grammar not found'}), 404
    
@bp.route('/score', methods=['POST'])
def score_grammar():
    """Score a grammar."""
    data = request.json
    grammar_id = data['grammar_id']
    success = data['success'].lower() == "true"

    grammar = grammar_service.update_score(grammar_id, success)
    
    if grammar:
        return jsonify({
            'success': True,
            'grammar': grammar.to_dict(include_relationships=False)
        })
    else:
        return jsonify({'error': 'grammar not found'}), 404