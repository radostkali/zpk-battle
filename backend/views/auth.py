from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_required

from daos import AuthDAO
from services import LoginService

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not (username and password):
        return jsonify({'error': 'Для входа в аккаунт укажите никнэйм и пароль'}), 400

    login_service = LoginService(auth_dao=AuthDAO())
    login_response = login_service.execute(
        username=username,
        password=password,
    )

    if not login_response.is_logged_in:
        return jsonify({'error': login_response.error}), 400

    return 'OK', 200


@login_required
@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return 'OK', 200
