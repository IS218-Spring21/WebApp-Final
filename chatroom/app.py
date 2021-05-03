"""
Chatroom Application
"""
import datetime
import redis
from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
)

app = Flask(__name__)
app.secret_key = 'asdf'
r = redis.StrictRedis('redis', 6379, 0, charset='utf-8', decode_responses=True)

def event_stream():
    """
    Handles Messages being sent into redis
    """
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('chat')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles User login
    """
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect('/')
    return render_template('login.html')


@app.route('/post', methods=['POST'])
def post():
    """
    Posts user's messages
    """
    message = request.form['message']
    user = session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    r.publish('chat', '[%s] %s: %s' % (now.isoformat(), user, message))
    return Response(status=204)


@app.route('/stream')
def stream():
    """
    Handles streaming the messages into the chatroom
    """
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/')
def home():
    """
    Displays the chatroom. If user isn't logged in it will redirect them to the login page
    """
    if 'user' not in session:
        return redirect('/login')
    return render_template('chat.html', user=session['user'])


if __name__ == '__main__':
    app.run()
