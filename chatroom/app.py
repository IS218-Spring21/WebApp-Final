"""
Chatroom Application using Redis & SocketIO
"""
import os
import redis
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://redis')

server_session = Session(app)
socketIO = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Displays Index.html
    """
    return render_template('index.html')


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    """
    Main chatroom
    """
    if request.method == "POST":
        username = request.form['username']
        room = request.form['roomName']
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)

    if session.get('username') is not None:
        return render_template('chat.html', session=session)

    return redirect(url_for('index'))


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


if __name__ == '__main__':
    socketIO.run(app, host='0.0.0.0', port=5000)
