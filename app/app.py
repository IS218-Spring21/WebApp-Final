# Python standard libraries
import os
import sqlite3

# Third party libraries
from flask import Flask
from flask_login import (
    LoginManager,
)

# Internal imports
from main.db import init_db_command
from main.user import User

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
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
    return User.get(user_id)


with app.app_context():
    from app.main import main_routes

    app.register_blueprint(main_routes.main_page)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context="adhoc")
