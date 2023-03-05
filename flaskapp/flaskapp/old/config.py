"""Flask configuration"""
from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))

# if you are not using docker you might want to use load_dotenv to load environment variables
#load_dotenv(path.join(basedir, ".env"))


class Config():
    """common config to all"""
    SECRET_KEY = environ.get("SECRET_KEY")
    # adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
    PYTHONUNBUFFERED = True


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    # LEVEL is overridden by loglevel for gunicorn.conf.py
    LEVEL = "WARNING"
    CONNECTSTRING=environ.get("CONNECTSTRING_PRODUCTION")

class DevConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True
    LEVEL = "DEBUG"
    CONNECTSTRING=environ.get("CONNECTSTRING_DEVELOPMENT")


"""
Usage of the above
-------------------
In app.py
     app.config.from_object('config.ProdConfig')
or
     app.config.from_object('config.DevConfig')
Both of these classes extend the base config Config
"""
