from datetime import datetime
from typing import Optional

import click
from flask.cli import with_appcontext

from app import db
from models import Round
from models.round import RoundTypes


@click.command('create_round')
@click.argument('number')
@click.argument('theme')
@click.argument('round_type')
@click.argument('last_day')
@click.argument('style', required=False)
@with_appcontext
def create_round(number: int, theme: str, round_type: str, last_day: str, style: Optional[str]):
    """ Creates new battle round """
    round_types = set(item.value for item in RoundTypes)
    if round_type not in round_types:
        click.echo('Round type should be one of this: {}'.format(round_types))
        return

    try:
        last_day = datetime.strptime(last_day, '%d-%m-%Y').date()
    except ValueError:
        click.echo('Provide last day of round in format: day-month-year. Example: 01-12-2021')
        return

    new_round = Round(
        number=number,
        theme=theme,
        style=style,
        type=round_type,
        last_day=last_day,
    )

    db.session.add(new_round)
    db.session.commit()
    click.echo('Round created')
