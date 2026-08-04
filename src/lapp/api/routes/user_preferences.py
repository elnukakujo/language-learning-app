from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import logging
logger = logging.getLogger(__name__)

from ...schemas.system_data import UserPreferencesDict
from ...services.system_data import UserPreferencesService
user_preferences_service = UserPreferencesService()

bp = Blueprint('user_preferences', __name__, url_prefix='/api/pref')

@bp.route('/<pref_id>', methods=['GET'])
def get_user_preferences(pref_id: str):
    """
    Get a specific user preferences by ID
    ---
    tags:
      - UserPreferences
    parameters:
      - name: pref_id
        in: path
        type: string
        required: true
        description: The ID of the user preferences to retrieve
    responses:
      200:
        description: User preferences object
        schema:
          type: object
      404:
        description: User preferences not found
    """
    user = user_preferences_service.get_by_id(pref_id, as_dict=True)
    
    if not user:
        return jsonify({'error': 'User preferences not found'}), 404
    
    return jsonify(user)

@bp.route('/', methods=['POST'])
def create_user_preferences():
    """
    Create user preferences
    ---
    tags:
      - UserPreferences
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              example: "user_U0
            native_language_iso639_2:
              type: array
              items:
                type: string
                example: "eng"
            learning_goals:
              type: string
              example: "Improve vocabulary"
            preferred_exercise_types:
              type: array
              items:
                type: string
                example: "translate"
    responses:
        201:
            description: User preferences created successfully
            schema:
            type: object
        400:
            description: Invalid input data
    """
    try:
        # Validate request data
        data = UserPreferencesDict(**request.json)
        
        # Create user
        pref = user_preferences_service.create(data, as_dict=True)
        
        if pref:
            return jsonify({
                'success': True,
                'user_preferences': pref
            }), 201
        else:
            return jsonify({'error': 'Failed to create user preferences'}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400
    
@bp.route('/<pref_id>', methods=['PUT', 'PATCH'])
def update_user_preferences(pref_id: str):
    """Update a user preferences.
    ---
    tags:
      - UserPreferences
    parameters:
      - name: pref_id
        in: path
        type: string
        required: true
        description: The ID of the user preferences to update
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                user_id:
                    type: string
                    example: "user_U0"
                native_language_iso639_2:
                    type: array
                    items:
                        type: string
                        example: "eng"
                learning_goals:
                    type: string
                    example: "Improve vocabulary"
                preferred_exercise_types:
                    type: array
                    items:
                        type: string
                        example: "translate"
    responses:
      200:
        description: User preferences updated successfully
        schema:
          type: object
          schema:
            type: object
            properties:
                success:
                    type: boolean
                    example: true
                    description: Indicates if the update was successful
                user_preferences:
                    type: object
                    description: The updated user preferences object
      400:
        description: Validation failed
      404:
        description: User preferences not found
    """
    try:
        data = UserPreferencesDict(**request.json)
        
        pref = user_preferences_service.update(pref_id, data, as_dict=True)
        
        if pref:
            return jsonify({
                'success': True,
                'user_preferences': pref
            })
        else:
            return jsonify({'error': 'User preferences not found'}), 404
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400
    
@bp.route('/<pref_id>', methods=['DELETE'])
def delete_user_preferences(pref_id: str):
    """Delete a user preferences.
    ---
    tags:
      - UserPreferences
    parameters:
      - name: pref_id
        in: path
        type: string
        required: true
        description: The ID of the user preferences to delete
    responses:
        204:
            description: User preferences deleted successfully
        404:
            description: User preferences not found
    """
    success = user_preferences_service.delete(pref_id)

    if success:
        return jsonify({'success': True}), 204
    else:
        return jsonify({'error': 'User preferences not found'}), 404


@bp.route('/test-endpoint', methods=['POST'])
def test_endpoint():
    """Test connectivity to an API endpoint (server-side, no CORS)."""
    import time, urllib.request

    body = request.json or {}
    base_url = (body.get("base_url") or "").strip()
    if not base_url:
        return jsonify({"ok": False, "error": "No base URL provided"}), 400

    url = f"{base_url.rstrip('/')}/models"
    req = urllib.request.Request(url, method="GET")
    if body.get("api_key"):
        req.add_header("Authorization", f"Bearer {body['api_key']}")

    start = time.perf_counter()
    try:
        urllib.request.urlopen(req, timeout=5)
        ms = round((time.perf_counter() - start) * 1000)
        return jsonify({"ok": True, "ms": ms})
    except Exception as e:
        ms = round((time.perf_counter() - start) * 1000)
        return jsonify({"ok": False, "ms": ms, "error": str(e)})