from flask import Blueprint, jsonify, request

import logging

from ...services.data_collection import DailyStatsService

logger = logging.getLogger(__name__)

bp = Blueprint('daily_stats', __name__, url_prefix='/api/daily-stats')
daily_stats_service = DailyStatsService()


@bp.route('/me/today', methods=['GET'])
def get_my_daily_stats_today():
    """Get today's daily stats for the current user and language.
    ---
    tags:
      - daily-stats
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
      - name: language_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Daily stats object
    """
    user_id = request.args.get('user_id')
    language_id = request.args.get('language_id')

    if not user_id or not language_id:
        return jsonify({'error': 'user_id and language_id are required'}), 400

    daily_stats = daily_stats_service.get_today_for_user(
        user_id=user_id,
        language_id=language_id,
        as_dict=True,
        include_relations=False,
    )
    return jsonify(daily_stats)


@bp.route('/<daily_stats_id>', methods=['GET'])
def get_daily_stats_by_id(daily_stats_id: str):
    """Get a single daily stats entry by ID.
    ---
    tags:
      - daily-stats
    parameters:
      - name: daily_stats_id
        in: path
        type: string
        required: true
      - name: user_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Daily stats object
      403:
        description: Forbidden
      404:
        description: Not found
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    daily_stats = daily_stats_service.get_by_id(
        daily_stats_id=daily_stats_id,
        as_dict=True,
        include_relations=False,
    )

    if not daily_stats:
        return jsonify({'error': 'Daily stats not found'}), 404

    if daily_stats.get('user_id') != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    return jsonify(daily_stats)