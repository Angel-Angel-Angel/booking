from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    def __repr__(self):
        return f"<User {self.email}, role={self.role}>"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default="Booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='bookings', lazy=True)

    def __repr__(self):
        return f"<Booking {self.service} {self.date} {self.time_slot}>"

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(50))
    to = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    work_performed_at = db.Column(db.String(200))
    address = db.Column(db.String(200))

    description = db.Column(db.Text)
    price = db.Column(db.Float)
    total = db.Column(db.Float)

    terms = db.Column(db.Text)

    signature_name = db.Column(db.String(100))
    signature_date = db.Column(db.String(50))

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

