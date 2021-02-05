from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_required, current_user

from daos import AuthDAO
from exceptions import LoginException
from services import LoginService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api')


@auth_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'color': f'#{current_user.color}',
    }), 200


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not (username and password):
        return jsonify({'error': 'Для входа в аккаунт укажите никнэйм и пароль'}), 400

    login_service = LoginService(auth_dao=AuthDAO())
    try:
        user_entity = login_service.execute(
            username=username,
            password=password,
        )
    except LoginException as e:
        return jsonify({'error': e.message}), 400

    return jsonify({
        'id': user_entity.pk,
        'username': user_entity.username,
    }), 200


@login_required
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'status': 'OK'}), 200
