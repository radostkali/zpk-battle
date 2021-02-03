import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from app import db
from models import User


@click.command('create_user')
@click.argument('username')
@click.argument('password')
@click.argument('color')
@with_appcontext
def create_user(username: str, password: str, color: str):
    """ Register new user """
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo('User with this username already exists.')
        return

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(
        username=username,
        password=hashed_password,
        color=color,
    )

    db.session.add(new_user)
    db.session.commit()
    click.echo('User created')
