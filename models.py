from app import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    order_received = db.Column(db.Boolean, default=False)
    order_confirmed = db.Column(db.Boolean, default=False)
