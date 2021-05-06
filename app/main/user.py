"""
Makes a new user in the Database
"""
from flask_login import UserMixin

from .db import get_db


class User(UserMixin):
    """
    User class
    """

    def __init__(self, id_, name, email, profile_pic):
        self.usr_id = id_  # changed from id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        """
        gets a user
        :param user_id: user unique id
        :return: user from the database
        """
        user_db = get_db()
        user = user_db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        """
        Creates a new user
        :param id_: user id
        :param name: user name
        :param email: user email
        :param profile_pic: user pic
        :return: creates a user
        """
        user_db = get_db()
        user_db.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        user_db.commit()
