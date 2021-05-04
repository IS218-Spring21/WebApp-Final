from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

# https://www.youtube.com/watch?v=q42zgGaYYzE

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'  # TODO: Change this to redis

Session(app)


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


if __name__ == '__main__':
    app.run()
