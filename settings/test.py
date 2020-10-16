import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
TESTING = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite://"
WTF_CSRF_ENABLED = False
