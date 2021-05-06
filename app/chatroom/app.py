# """
# Chatroom Application using Redis & SocketIO
# """
# import os
# import redis
# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_socketio import SocketIO, join_room, leave_room, emit
# from flask_session import Session
#
#
# app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.from_url('redis://redis')
#
# server_session = Session(app)
# socketIO = SocketIO(app, manage_session=False)
#
#
#
#
# if __name__ == '__main__':
#     socketIO.run(app)
