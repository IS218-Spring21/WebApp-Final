from flask import Blueprint
from . import routes, events

chatroom = Blueprint('chatroom', __name__)
