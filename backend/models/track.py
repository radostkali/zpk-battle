from app import db


class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    rates = db.relationship('Rate', back_populates='track')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tracks')

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    round = db.relationship('Round', back_populates='tracks')
