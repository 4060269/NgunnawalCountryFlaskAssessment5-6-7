from app import db                 # get access to the db by creating instance
from datetime import datetime      # create an instance of real-time

class Contact(db.Model):                                             # class is to store db in memory
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # first variable is an entry
    name = db.Column(db.Text)                                        # it is defined as a column in db
    email = db.Column(db.Text)                                       # the last variable is data type defined in db
    message = db.Column(db.Text)
    dateSubmitted = db.Column(db.DateTime)

    def __init__(self, name, email, message):                        # auto runs when new contact created,
        self.name = name                                             # these are initalizaing the objects attriututes
        self.email = email                                           # this is always needed for any object created from a class
        self.message = message
        self.dateSubmitted = datetime.today()                        # this line sets the datetime to be taken from the local computers date & time

class todo(db.Model):                                                # same thing as contact class
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # less entries and still auto creates a new id for every entry
    text = db.Column(db.Text)                                        # I don't 'create' the init but it is still there
    done = db.Column(db.Boolean)