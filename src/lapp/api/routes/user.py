from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import logging
logger = logging.getLogger(__name__)

from ...schemas.system_data import UserDict
from ...services.system_data import UserService
user_service = UserService()

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of user objects
        schema:
          type: array
          items:
            type: object
    """
    users = user_service.get_all(as_dict=True)
    return jsonify(users)


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id: str):
    """
    Get a specific user by ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user to retrieve
    responses:
      200:
        description: User object
        schema:
          type: object
      404:
        description: User not found
    """
    user = user_service.get_by_id(user_id, as_dict=True)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user)


@bp.route('/', methods=['POST'])
def create_user():
    """Create a new user.
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    example: "john_doe"
                    description: The unique username for the user
                    required: true
    responses:
      201:
        description: Language created successfully
        schema:
          type: object
      400:
        description: Validation failed or creation error
    """
    try:
        # Validate request data
        data = UserDict(**request.json)
        
        # Create user
        user = user_service.create(data, as_dict=True)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id: str):
    """Update a user.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user to update
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    example: "john_doe_updated"
                    description: The new username for the user
                    required: false
    responses:
      200:
        description: User updated successfully
        schema:
          type: object
          schema:
            type: object
            properties:
                success:
                    type: boolean
                    example: true
                    description: Indicates if the update was successful
                user:
                    type: object
                    description: The updated language object
      400:
        description: Validation failed
      404:
        description: Language not found
    """
    try:
        data = UserDict(**request.json)
        
        user = user_service.update(user_id, data, as_dict=True)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            })
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Delete a user.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user to delete
    responses:
        204:
            description: User deleted successfully
        404:
            description: User not found
    """
    success = user_service.delete(user_id)
    
    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'User not found'}), 404