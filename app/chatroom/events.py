from flask import session
from flask_socketio import emit, join_room, leave_room
from ..app import socketIO


@socketIO.on('join', namespace='/chatroom')
def join():
    """
    Displays text when a user joins a room
    """
    room = session.get('room')
    join_room(room)
    emit('status',
         {'msg': "%s has entered the room." % (session.get('username'))},
         room=room)


@socketIO.on('message', namespace='/chatroom')
def text(message):
    """
    Displays text when a user sends a message
    """
    room = session.get('room')
    emit('message',
         {'msg': "%s : %s" % (session.get('username'), message['msg'])},
         room=room)


@socketIO.on('left', namespace='/chatroom')
def left():
    """
    Displays text when a user leaves a room
    """
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': "%s has left the room." % username}, room=room)