"""Flask config."""

from os import environ, path
from dotenv import load_dotenv

# basedir just gets the current working directory
basedir = path.abspath(path.dirname(__file__))
# path.join makes something like this 'roomly/.env'. 
# This points to the .env file in the root folder"""
load_dotenv(path.join(basedir, '.env'))


# I got this off the internet. But basically create a class Config with all
# the flask configuration
class Config:

    # Set Flask config Variables

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SECRET_KEY = environ.get('APP_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    MYSQL_HOST = environ.get('MYSQL_HOST')
    MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    MYSQL_DB = environ.get('MYSQL_DB')