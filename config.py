import os
# Need to interact with clients OS to get time,

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'ngunnawal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# this stuff is creating an object for the db and yeah......
