"""
Is used to make model for database
"""
from flask import current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy

database_blueprint = Blueprint('database', __name__)
current_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:password@postgres:5432/root'
database = SQLAlchemy(current_app)
database.create_all()


class UserModel(database.Model):
    """
    UserModel for database
    """
    user_id = database.Column(database.String(255), primary_key=True)
    user_name = database.Column(database.String(255), nullable=False)
    user_email = database.Column(database.String(255), unique=True, nullable=False)
    user_profile_pic = database.Column(database.String(255), nullable=False)

    def __repr__(self):
        return '<User %r' % self.user_name


def get_database():
    """
    returns all the database information
    """
    return UserModel.query().all()
