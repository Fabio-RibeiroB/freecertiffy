from flask import Flask
import cert_blueprint_routes
import login_blueprint_routes
import users_blueprint_routes
import logging
import os
app = Flask(__name__)

# Align logging between gunicorn and flask
gunicorn_logger = logging.getLogger("gunicorn.error")
if logging.getLevelName(gunicorn_logger.level) != "NOTSET":
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    LEVEL = f"{logging.getLevelName(gunicorn_logger.level)}"
    logging.basicConfig(
        level=eval("logging." + LEVEL),
        format="playpit %(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
else:
    #  if gunicorn settings dont direct
    LEVEL = os.environ["LEVEL"]
    logging.basicConfig(
        format="freecertiffy %(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
    logging.getLogger().setLevel(eval("logging." + LEVEL))

# Using Session for logins and authorisation
app.secret_key = os.environ['SECRET_KEY']
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False

# Register blueprints (views/routes)
app.register_blueprint(cert_blueprint_routes.cert_blueprint_routes, url_prefix="/")
app.register_blueprint(login_blueprint_routes.login_blueprint_routes, url_prefix="/login")
app.register_blueprint(users_blueprint_routes.users_blueprint_routes, url_prefix="/user")
