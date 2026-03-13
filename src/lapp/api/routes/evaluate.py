from flask import Blueprint, request

from ...services import EvaluatorService

bp = Blueprint('evaluate', __name__, url_prefix='/api/evaluate')
evaluator_service = EvaluatorService()

@bp.route('/translate', methods=['POST'])
def evaluate_translation():
    """Evaluate a translation for an exercise.
    ---
    tags:
        - Evaluation
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            description: Translation evaluation object
            properties:
                exercise_id:
                    type: string
                    example: "ex_E1"
                    description: "ID of the exercise to evaluate"
                    required: true
                user_translation:
                    type: string
                    example: "Hello, my name is John."
                    description: "The user's translation"
                    required: true
    responses:
        200:
            description: Translation evaluated successfully
            schema:
                type: object
                description: Evaluation result object with score and tokens information
        404:
            description: Exercise not found or translation evaluation failed
    """
    data = request.json

    return evaluator_service.evaluate_translation(
        ex_id=data['exercise_id'],
        user_translation=data['user_translation']
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

    return evaluator_service.evaluate_speech(
        ex_id=data['exercise_id'],
        user_audio_url=data['user_audio_url']
    )