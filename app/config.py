from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))
load_dotenv(path.join(basedir, '.env'))

# Setting up the configuration variables
class Config:
    MYSQL_DATABASE = environ["MYSQL_DATABASE"]
    MYSQL_USER = environ["MYSQL_USER"]
    MYSQL_PASSWORD = environ["MYSQL_PASSWORD"]
    MYSQL_PORT = environ["MYSQL_PORT"]
    MYSQL_HOST = environ["MYSQL_HOST"]
    DEBUG = environ["DEBUG"]
    FLASK_DEBUG=environ["FLASK_DEBUG"]
    PORT = environ["PORT"]
    HOST = environ["HOST"]
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
