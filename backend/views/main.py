from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from daos import BattleDataDAO, BattleControlDAO
from exceptions import SubmitTrackException
from services import FetchBattleDataService, SubmitTrackService, ToggleRateService


main_blueprint = Blueprint('main', __name__, url_prefix='/api')


@main_blueprint.route('/battle-data', methods=['GET'])
def battle_data():
    fetch_battle_data_service = FetchBattleDataService(battle_data_dao=BattleDataDAO())
    battle_data_dict = fetch_battle_data_service.execute()
    return jsonify(battle_data_dict), 200


@main_blueprint.route('/submit-track', methods=['POST'])
@login_required
def submit_track():
    round_id = request.json.get('roundId')
    track_name = request.json.get('name')
    user_id = current_user.id

    if not (round_id or track_name):
        return jsonify({'error': 'Для подачи трэка нужно указать его название'}), 400

    submit_track_service = SubmitTrackService(battle_control_dao=BattleControlDAO())
    try:
        submit_track_service.execute(
            round_id=round_id,
            track_name=track_name,
            user_id=user_id,
        )
    except SubmitTrackException as e:
        return jsonify({'error': e.message}), 400

    return jsonify({'status': 'OK'}), 200


@main_blueprint.route('/toggle-rate', methods=['POST'])
@login_required
def toggle_rate():
    round_id = request.json.get('roundId')
    category_id = request.json.get('categoryId')
    track_id = request.json.get('trackId')
    user_id = current_user.id

    if not (round_id or category_id or track_id):
        return jsonify({'error': 'Для выставления оценки нужно указать roundId, categoryId, trackId'}), 400

    toggle_rate_service = ToggleRateService(battle_control_dao=BattleControlDAO())
    toggle_rate_service.execute(
        round_id=round_id,
        category_id=category_id,
        track_id=track_id,
        user_id=user_id,
    )

    return jsonify({'status': 'OK'}), 200
