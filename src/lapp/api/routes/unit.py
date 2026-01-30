from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ...services import UnitService
from ...schemas.element_dict import UnitDict

bp = Blueprint('unit', __name__, url_prefix='/api/units')
unit_service = UnitService()

@bp.route('/all/<language_id>', methods=['GET'])
def get_all_units(language_id: str):
    """Get all units.
    ---
    tags:
        - Units
    parameters:
        - name: language_id
          in: path
          type: string
          required: true
          description: The ID of the language to retrieve units from
    responses:
        200:
            description: List of units
            schema:
                type: array
                items:
                    type: object
                    description: Unit object
    """
    units = unit_service.get_all(language_id = language_id)
    return jsonify([unit.to_dict() for unit in units])


@bp.route('/<unit_id>', methods=['GET'])
def get_unit(unit_id: str):
    """Get a specific unit by ID.
    ---
    tags:
        - Units
    parameters:
        - name: unit_id
          in: path
          type: string
          required: true
          description: The ID of the unit to retrieve
    responses:
        200:
            description: Unit object
            schema:
                type: object
        404:
            description: Unit not found
    """
    unit = unit_service.get_by_id(unit_id)
    
    if not unit:
        return jsonify({'error': 'Unit not found'}), 404
    
    return jsonify(unit.to_dict())


@bp.route('/', methods=['POST'])
def create_unit():
    """Create a new unit.
    ---
    tags:
      - Units
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                language_id:
                    type: string
                    required: true
                    description: The ID of the language the unit belongs to
                    example: "lang_L1"
                title:
                    type: string
                    required: true
                    description: The title of the unit
                    example: "Basic Phrases"
                description:
                    type: string
                    required: false
                    description: A brief description of the unit
                    example: "This unit covers basic phrases in the language."
                level:
                    type: string
                    required: false
                    description: The proficiency level of the unit
                    example: "A1"
    responses:
        201:
            description: Unit created successfully
            schema:
                type: object
                properties:
                    success:
                        type: boolean
                    unit:
                        type: object
                        description: The created unit object
        400:
            description: Validation error
            properties:
                error:
                    type: string
                    description: Error message
                details:
                    type: array
                    description: List of validation errors
    """
    try:
        # Validate request data
        data = UnitDict(**request.json)
        
        # Create unit
        unit = unit_service.create(data)
        
        if unit:
            return jsonify({
                'success': True,
                'unit': unit.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create unit'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<unit_id>', methods=['PUT', 'PATCH'])
def update_unit(unit_id: str):
    """Update a unit.
    ---
    tags:
      - Units
    parameters:
      - name: unit_id
        in: path
        type: string
        required: true
        description: The ID of the unit to update
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                language_id:
                    type: string
                    description: The ID of the language the unit belongs to
                    required: true
                    example: "lang_L1"
                title:
                    type: string
                    description: The title of the unit
                    required: true
                    example: "Basic Phrases"
                description:
                    type: string
                    description: A brief description of the unit
                    required: false
                    example: "This unit covers basic phrases in the language."
                level:
                    type: string
                    description: The proficiency level of the unit
                    required: false
                    example: "A1" 
    """
    try:
        data = UnitDict(**request.json)
        
        unit = unit_service.update(unit_id, data)
        
        if unit:
            return jsonify({
                'success': True,
                'unit': unit.to_dict()
            })
        else:
            return jsonify({'error': 'Unit not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<unit_id>', methods=['DELETE'])
def delete_unit(unit_id: str):
    """Delete a unit.
    ---
    tags:
      - Units
    parameters:
      - name: unit_id
        in: path
        type: string
        required: true
        description: The ID of the unit to delete
    responses:
        204:
            description: Unit deleted successfully
        404:
            description: Unit not found
    """
    success = unit_service.delete(unit_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'Unit not found'}), 404