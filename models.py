from app import db
from datetime import datetime

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)
    dateSubmitted = db.Column(db.DateTime)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
        self.dateSubmitted = datetime.today()

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)