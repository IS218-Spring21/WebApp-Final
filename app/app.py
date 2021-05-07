"""
PUT DOCSTRING HERE
"""
# Python standard libraries
import os
import sqlite3
import redis
import eventlet

# Third party libraries
from flask import Flask
from flask_login import (
    LoginManager,
)
from flask_session import Session
from flask_socketio import SocketIO

# Internal imports
from main.user import User
from main.db import init_db_command


# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://redis')

server_session = Session(app)
socketIO = SocketIO()

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Sends unauthorized to client
    """
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    """
    Returns user_id to back-end
    """
    return User.get(user_id)


with app.app_context():
    from app.main import main_routes

    app.register_blueprint(main_routes.main_page)

with app.app_context():
    from chatroom import chatroom

    app.register_blueprint(chatroom)

if __name__ == "__main__":
    socketIO.init_app(app, manage_session=False)
    eventlet.wrap_ssl(socketIO.run(app, debug=True, host='0.0.0.0', port=443, ssl_context='adhoc'))
