'''Routes for Main Page'''

# Python standard libraries
import json
# import os

# Third-party libraries
from flask import redirect, request, url_for, render_template, Response, session
from flask import Blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from .db import get_db
from .user import User

main_page = Blueprint(
    'main_page',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Configuration
GOOGLE_CLIENT_ID = "328754940117-blnf0979a5plol9qphredrdntpgmrsp9.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "HpeG2-6H1vj3NSTsnvYv0jdj"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@main_page.route("/")
def index():
    """This method is the main page for our web app

    If the user is logged in:
    :return: this will return the main page with the logged in users, if not,
    it will return the default logged out page.
    """
    session['is_auth'] = current_user.is_authenticated
    if session.get('is_auth'):
        cur_name = current_user.name
        cur_email = current_user.email
        cur_pic = current_user.profile_pic
        return render_template("index.jinja2", is_auth=session.get('is_auth'),
                               cur_name=cur_name, cur_email=cur_email,
                               cur_pic=cur_pic)
    return render_template("index.jinja2", is_auth=session.get('is_auth'))


def get_google_provider_cfg():
    """
    Gets google provider cfg
    :return: google provider cfg
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@main_page.route("/login")
def login():
    """
    Routes the user to google login page
    :return: The user can login with their google account
    """
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@main_page.route("/login/callback")
def callback():
    """

    :return:
    """
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("main_page.index"))


@main_page.route("/logout")
@login_required
def logout():
    """

    :return:
    """
    logout_user()
    return redirect(url_for("main_page.index"))


@main_page.route("/api/users")
def api_browse() -> str:
    """

    :return:
    """
    data = []
    users_db = get_db().cursor()
    users_db.execute('SELECT * FROM user')
    result = users_db.fetchall()
    for row in result:
        data.append(list(row))
    json_result = json.dumps(data)
    resp = Response(json_result, status=200, mimetype="application/json")
    return resp
