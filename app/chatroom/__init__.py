"""
Main python file to pull other scripts into this one
"""
from flask import Blueprint, session, redirect, url_for, render_template, request
from . import events

chatroom = Blueprint('chatroom', __name__)


@chatroom.route('/chatroom/', methods=['GET', 'POST'])
def chatroom_index():
    """
    Displays Index.html
    """
    return render_template('index.html')


@chatroom.route('/chatroom/main', methods=['GET', 'POST'])
def chatroom_main():
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

    return redirect(url_for('chatroom'))
