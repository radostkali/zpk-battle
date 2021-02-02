import enum

from app import db


class RoundTypes(enum.Enum):
    all_vs_all = 'all_vs_all'
    one_vs_one = 'one_vs_one'


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, default=1)
    theme = db.Column(db.String(300), nullable=False)
    style = db.Column(db.String(100), nullable=True)
    type = db.Column(db.Enum(RoundTypes), default=RoundTypes.all_vs_all)
    last_day = db.Column(db.Date)

    tracks = db.relationship('Track', back_populates='round')
    rates = db.relationship('Rate', back_populates='round')
