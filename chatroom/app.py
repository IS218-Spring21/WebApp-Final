from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

# https://www.youtube.com/watch?v=q42zgGaYYzE

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'  # TODO: Change this to redis

Session(app)
socketIO = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if request.method == "POST":
        username = request.form['username']
        room = request.form['roomName']
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)
    else:
        if session.get('username') is not None:
            return render_template('chat.html', session=session)
        return redirect(url_for('index'))


@socketIO.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': "%s has entered the room.".format(session.get('username'))}, room=room)


@socketIO.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': "%s : %s".format(session.get('username'), message['msg'])}, room=room)


@socketIO.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': "%s has left the room.".format(session.get('username'))}, room=room)


if __name__ == '__main__':
    socketIO.run(app)
