"""
PUT DOCSTRING HERE
"""
# Python standard libraries
import os
import redis

# Third party libraries
from flask import Flask
from flask_login import (
    LoginManager,
)
from flask_session import Session
from flask_socketio import SocketIO

# Internal imports


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


with app.app_context():
    from app.auth0 import main_page
    from app.chatroom import chatroom
    from app.database import database_blueprint
    from app.database.user import User

    app.register_blueprint(main_page) #change to auth0 package
    app.register_blueprint(chatroom)
    app.register_blueprint(database_blueprint)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    """
    Returns user_id to back-end
    """
    return User.get(user_id)


if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=443, ssl_context="adhoc")
    socketIO.init_app(app, manage_session=False)
    socketIO.run(app, debug=True, host='0.0.0.0', port=443, ssl_context="adhoc")
    # eventlet.wrap_ssl(socketIO.run(app, debug=True, host='0.0.0.0', port=443, ssl_context="adhoc"))
