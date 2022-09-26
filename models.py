from app import db, login          # get access to the db by creating instance
from datetime import datetime      # create an instance of real-time
from flask_login import UserMixin  # imports userMixin, provides default values for user objects
from werkzeug.security import generate_password_hash, check_password_hash   # import from werkzeug security to give hashing functionality

class Contact(db.Model):    # class is to store db in memory
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # equates the database values to simple variables
    name = db.Column(db.Text)   # these variables are stored under the contact class
    email = db.Column(db.Text)  #
    message = db.Column(db.Text)    #
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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    user_level = db.Column(db.Integer)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_admin(self):
        if self.user_level == 2:
            return True
        else:
            return False

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def update_details(self, email_address, name):
    self.email_address = email_address
    self.name = name

class Photos(db.Model):
    photoid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    userid = db.Column(db.Integer)
    dateSubmitted = db.Column(db.DateTime)
    def __init__(self, title, filename, userid):
        self.title = title
        self.filename = filename
        self.userid = userid
        self.dateSubmitted = datetime.today()
