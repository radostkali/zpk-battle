from flask import Blueprint, jsonify
from flask_login import login_required, current_user

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return 'Index'


@login_required
@main_blueprint.route('/profile')
def profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
    }), 200
