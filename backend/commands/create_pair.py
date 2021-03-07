from datetime import datetime
from typing import Optional

import click
from flask.cli import with_appcontext

from app import db
from models import Round, Pair, User
from models.round import RoundTypes


@click.command('create_pair')
@click.argument('round_id')
@click.argument('user_one_id')
@click.argument('user_two_id')
@click.argument('user_three_id', required=False)
@with_appcontext
def create_pair(round_id: int, user_one_id: int, user_two_id: int, user_three_id: Optional[int]):
    """ Creates new pair for battle round """
    round = Round.query.get(round_id)
    if not round or round.type.value != RoundTypes.one_vs_one.value:
        one_vs_one_rounds = Round.query.filter_by(type=RoundTypes.one_vs_one.value)
        id_name_rounds_list = [
            '{} [id {}]'.format(round.theme, round.id)
            for round in one_vs_one_rounds
        ]
        click.echo('Pairs allows only for one vs one round type. Rounds allowed:')
        click.echo(', '.join(id_name_rounds_list))
        return

    user_one = User.query.get(user_one_id)
    user_two = User.query.get(user_two_id)
    user_three = user_three_id and User.query.get(user_three_id)
    if not user_one or not user_two or (user_three_id and not user_three):
        users = User.query.all()
        id_name_users_list = [
            '{} [id {}]'.format(user.username, user.id)
            for user in users
        ]
        click.echo('User not found. Users allowed:')
        click.echo(', '.join(id_name_users_list))
        return

    new_pair = Pair(
        user_one_id=user_one_id,
        user_two_id=user_two_id,
        user_three_id=user_three_id,
        round_id=round_id,
    )

    db.session.add(new_pair)
    db.session.commit()
    click.echo('Pair created')
