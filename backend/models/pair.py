from app import db


class Pair(db.Model):
    __tablename__ = 'pair'

    id = db.Column(db.Integer, primary_key=True)

    user_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_one = db.relationship('User', foreign_keys=[user_one_id])

    user_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_two = db.relationship('User', foreign_keys=[user_two_id])

    user_three_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_three = db.relationship('User', foreign_keys=[user_three_id])

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    round = db.relationship('Round', back_populates='pairs')
