from flask import Blueprint, request

from ...services import EvaluatorService

bp = Blueprint('evaluate', __name__, url_prefix='/api/evaluate')
evaluator_service = EvaluatorService()

@bp.route('/text', methods=['POST'])
def evaluate_text():
    """Evaluate a text answer for an exercise.
    ---
    tags:
        - Evaluation
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Text evaluation object
            properties:
                exercise_id:
                    type: string
                    example: "ex_E1"
                    description: "ID of the exercise to evaluate"
                    required: true
                user_text:
                    type: string
                    example: "Hello, my name is John."
                    description: "The user's text answer to evaluate"
                    required: true
    responses:
        200:
            description: Text evaluated successfully
            schema:
                type: object
                description: Evaluation result object with score and tokens information
        404:
            description: Exercise not found or text evaluation failed
    """
    data = request.json

    return evaluator_service.evaluate(
        ex_id=data['exercise_id'],
        user_input=data['user_text'],
        input_type='text'
    )

@bp.route('/speech', methods=['POST'])
def evaluate_speech():
    """Evaluate a speech answer for an exercise.
    ---
    tags:
        - Evaluation
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Speech evaluation object
            properties:
                exercise_id:
                    type: string
                    example: "ex_E1"
                    description: "ID of the exercise to evaluate"
                correct_audio_index:
                    type: integer
                    example: 0
                    description: "Index of the correct audio file to compare against (default is 0)"
                user_audio_url:
                    type: string
                    example: "/path/to/audio1.mp3"
                    description: "URL of the user's audio answer to evaluate"
    responses:
        200:
            description: Speech evaluated successfully
            schema:
                type: object
                description: Evaluation result object with score and feedback information
        404:
            description: Exercise not found or speech evaluation failed
    """
    data = request.json

    return evaluator_service.evaluate(
        ex_id=data['exercise_id'],
        user_input=data['user_audio_url'],
        input_type='speech',
        correct_audio_index=data.get('correct_audio_index', 0)
    )