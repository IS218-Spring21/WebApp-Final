"""
Main python file to pull other scripts into this one
"""
from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_login import current_user

chatroom = Blueprint('chatroom',
                     __name__,
                     template_folder='templates',
                     static_folder='static')


@chatroom.route('/chatroom', methods=['GET', 'POST'])
def chatroom_index():
    """
    Displays Index.html
    """
    if current_user.is_authenticated:
        return render_template('index.html', curr_name=current_user.name)
    return redirect(url_for('main_page.index'))


@chatroom.route('/chatroom/main', methods=['GET', 'POST'])
def chatroom_main():
    """
    Main chatroom
    """
    if current_user.is_authenticated:
        if request.method == "POST":
            username = current_user.name
            room = request.form['roomName']
            session['username'] = username
            session['room'] = room
            return render_template('chat.html', session=session)

    return redirect(url_for('chatroom.chatroom_index'))
