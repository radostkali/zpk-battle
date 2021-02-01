from app import db


class RateCategory(db.Model):
    __tablename__ = 'ratecategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, unique=True)
    rates = db.relationship('Rate', back_populates='category')
