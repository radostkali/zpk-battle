from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    tracks = db.relationship('Track', back_populates='user')
    rates = db.relationship('Rate', back_populates='user')
