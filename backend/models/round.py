from app import db


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(300), nullable=False)
    style = db.Column(db.String(100), nullable=True)
    tracks = db.relationship('Track', back_populates='round')
    rates = db.relationship('Rate', back_populates='round')
