# Models.py is used to define the db in the web app
# Allows us to, define meta-data, tables and fields in db

from app import db, login
# Get access to the db for tables and forms
from datetime import datetime
# Need to log messages with the current date and time
from flask_login import UserMixin
# Creates easier development with all the default values
from werkzeug.security import generate_password_hash, check_password_hash
# Import from werkzeug security to provide hashing functionality


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)
    dateSubmitted = db.Column(db.DateTime)
    # Class is to store db in memory
    # Need to have a model of db to take and send tables and fields
    # Equates the database values to simple local variables
    # To organize and re-send to database correctly

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
        self.dateSubmitted = datetime.today()
        # Needed to define datetime to be taken from the local computers date & time


class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)
    # Needed to create, track and determine whether an item is completed or not
    # Accessing columnar database


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    user_level = db.Column(db.Integer)
    # UserMixin is required to get properties of a user to be displayed

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        if self.user_level == 2:
            return True
        else:
            return False

    def update_details(self, email_address, name):
        self.email_address = email_address
        self.name = name


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Photos(db.Model):
    photoid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    userid = db.Column(db.Integer)
    dateSubmitted = db.Column(db.DateTime)
    #

    def __init__(self, title, filename, userid):
        self.title = title
        self.filename = filename
        self.userid = userid
        self.dateSubmitted = datetime.today()
        # Same as contact init, need to set date and time to client computer
