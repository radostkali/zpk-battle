from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_required

from daos import AuthDAO
from services import LoginService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not (username and password):
        return jsonify({'error': 'Для входа в аккаунт укажите никнэйм и пароль'}), 400

    login_service = LoginService(auth_dao=AuthDAO())
    login_response = login_service.execute(
        username=username,
        password=password,
    )

    if login_response.error:
        return jsonify({'error': login_response.error}), 400

    user_entity = login_response.user_entity
    return jsonify({
        'id': user_entity.pk,
        'username': user_entity.username,
    }), 200


@login_required
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'status': 'OK'}), 200
