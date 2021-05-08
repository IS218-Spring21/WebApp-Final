"""
Is used to make model for database
"""
from flask import current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy

database_blueprint = Blueprint('database', __name__)
# current_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://njpmnrxzhnwjpy:144bc3bd207debde9624ce611d1f265ebdac67f68fc5d89cf0f6b77547debba5@ec2-52-87-107-83.compute-1.amazonaws.com:5432/dd8pkj3btfpbud'
database = SQLAlchemy(current_app)
database.create_all()


class UserModel(database.Model):
    """
    UserModel for database
    """
    __tablename__ = 'Users'

    user_id = database.Column(database.String(255), primary_key=True)
    user_name = database.Column(database.String(255), nullable=False)
    user_email = database.Column(database.String(255), unique=True, nullable=False)
    user_profile_pic = database.Column(database.String(255), nullable=False)

    def __init__(self, user_id, user_name, user_email, user_profile_pic):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_profile_pic = user_profile_pic


    def __repr__(self):
        return '<id {}>'.format(self.id)


def get_database():
    """
    returns all the database information
    """
    return database.Query(UserModel).all()
