import os
# Need to interact with clients OS to get time, set paths and use crypto methods

basedir = os.path.abspath(os.path.dirname(__file__))
# Required for application and code to run properly


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Secure and represent users environmental variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'ngunnawal.db')
    # Use the db in root directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Unneeded feature turned off for better performance
