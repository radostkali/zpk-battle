import enum

from app import db


class Marks(enum.Enum):
    zero = 0
    one = 1


class Rate(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Enum(Marks), default=Marks.one)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='rates')

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    round = db.relationship('Round', back_populates='rates')

    category_id = db.Column(db.Integer, db.ForeignKey('ratecategory.id'))
    category = db.relationship('RateCategory', back_populates='rates')

    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    track = db.relationship('Track', back_populates='rates')
