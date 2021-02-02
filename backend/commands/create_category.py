import click
from flask.cli import with_appcontext

from app import db
from models import RateCategory


@click.command('create_category')
@click.argument('name')
@with_appcontext
def create_category(name: str):
    """ Creates new rate category """
    category = RateCategory.query.filter_by(name=name).first()
    if category:
        click.echo('Category with this name already exists.')
        return

    new_category = RateCategory(
        name=name,
    )

    db.session.add(new_category)
    db.session.commit()
    click.echo('Category created')
