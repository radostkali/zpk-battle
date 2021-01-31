from flask import Blueprint, jsonify
from flask_login import login_required, current_user

main_blueprint = Blueprint('main', __name__, url_prefix='/api')


@login_required
@main_blueprint.route('/profile', methods=['GET'])
def profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
    }), 200
