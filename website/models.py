from . import db
from datetime import datetime
from flask_login import UserMixin

# User table
class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(11)) 
    comments = db.relationship('Comment', backref='user')

# Event table
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    location = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    _status = db.Column('status', db.String(20), default="OPEN")
    date = db.Column(db.String(10))
    number_of_tickets = db.Column(db.Integer)
    ticket_price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')

    @property
    def status(self):
        event_date = datetime.strptime(self.date, "%d-%m-%Y").date()
        today = datetime.now().date()
        if event_date < today:
            return "INACTIVE"
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

# Book table
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_tickets = db.Column(db.Integer)
    total_cost = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship('Event', backref='book')

    def __repr__(self):
        return "<Booking ID: {}>".format(self.id)

# Comments table
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
