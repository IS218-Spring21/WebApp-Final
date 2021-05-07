"""
File used to maintain rows of UserModel
"""
from flask_login import UserMixin

from . import UserModel


class User(UserMixin):
    """
    User class
    """

    def __init__(self, user_id, user_name, user_email, user_profile_pic):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_profile_pic = user_profile_pic

    @staticmethod
    def get(user_id):
        """
        gets a user
        :param user_id: user unique id
        :return: user from the database
        """
        user = UserModel.query.filter_by(user_id=user_id).first()
        if not user:
            return None

        user = User(
            user_id=user[0], user_name=user[1], user_email=user[2], user_profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(user_id, user_name, user_email, user_profile_pic):
        """
        Creates a new user
        """
        UserModel.session.add(user_id, user_name, user_email, user_profile_pic)
        UserModel.session.commit()
