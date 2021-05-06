from flask import session, redirect, url_for, render_template, request
from . import chatroom

@chatroom.route('/chatroom/', methods=['GET', 'POST'])
def index():
    """
    Displays Index.html
    """
    return render_template('index.html')


@chatroom.route('/chatroom/main', methods=['GET', 'POST'])
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

    return redirect(url_for('index.html'))