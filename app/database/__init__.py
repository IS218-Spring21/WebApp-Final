from flask import current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy

database_blueprint = Blueprint('database', __name__)
current_app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/root'
database = SQLAlchemy(current_app)


class User(database.Model):
    user_id = database.Column(database.String(255), primary_key=True)
    user_name = database.Column(database.String(255), nullable=False)
    user_email = database.Column(database.String(255), unique=True, nullable=False)
    user_profile_pic = database.Column(database.String(255), nullable=False)

    def __repr__(self):
        return '<User %r' % self.user_name
