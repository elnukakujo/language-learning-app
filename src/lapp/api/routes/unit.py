from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import UnitService
from ...schemas.element_dict import UnitDict

bp = Blueprint('unit', __name__, url_prefix='/api/units')
unit_service = UnitService()

@bp.route('/', methods=['GET'])
def get_all_units():
    """Get all units."""
    units = unit_service.get_all()
    return jsonify([unit.to_dict(include_relationships=False) for unit in units])


@bp.route('/<unit_id>', methods=['GET'])
def get_unit(unit_id: str):
    """Get a specific unit by ID."""
    unit = unit_service.get_by_id(unit_id)
    
    if not unit:
        return jsonify({'error': 'Unit not found'}), 404
    
    return jsonify(unit.to_dict(include_relationships=True))


@bp.route('/', methods=['POST'])
def create_unit():
    """Create a new unit."""
    try:
        # Validate request data
        data = UnitDict(**request.json)
        
        # Create unit
        unit = unit_service.create(data)
        
        if unit:
            return jsonify({
                'success': True,
                'unit': unit.to_dict(include_relationships=False)
            }), 201
        else:
            return jsonify({'error': 'Failed to create unit'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<unit_id>', methods=['PUT', 'PATCH'])
def update_unit(unit_id: str):
    """Update a unit."""
    try:
        data = UnitDict(**request.json)
        
        unit = unit_service.update(unit_id, data)
        
        if unit:
            return jsonify({
                'success': True,
                'unit': unit.to_dict(include_relationships=True)
            })
        else:
            return jsonify({'error': 'Unit not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<unit_id>', methods=['DELETE'])
def delete_unit(unit_id: str):
    """Delete a unit."""
    success = unit_service.delete(unit_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'Unit not found'}), 404