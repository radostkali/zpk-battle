import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

sys.path.insert(1, os.path.abspath(os.getcwd()))

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        return User.query.get(int(user_id))

    # views
    from views.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from views.main import main_blueprint
    app.register_blueprint(main_blueprint)

    # commands
    from commands import create_user, create_category, create_round
    app.cli.add_command(create_user)
    app.cli.add_command(create_category)
    app.cli.add_command(create_round)

    return app
