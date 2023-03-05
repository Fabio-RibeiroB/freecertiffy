"""Flask configuration"""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
"""sensitive variables like tokens and connect strings in .env"""
load_dotenv(path.join(basedir, ".env"))


class Config:
    """common config to all"""
    SECRET_KEY = environ.get("SECRET_KEY")
    # adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
    PYTHONUNBUFFERED = True


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    # LEVEL is overridden by loglevel for gunicorn.conf.py
    LEVEL = "WARNING"

class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    LEVEL = "DEBUG"


"""
Usage of the above
-------------------
In app.py
     app.config.from_object('config.ProdConfig')
or
     app.config.from_object('config.DevConfig')
Both of these classes extend the base config Config
"""
