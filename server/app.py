"""
app.py

Initializes the application with the configuration and constructs the
RESTful API endpoints using the controllers.
"""
from flask import Flask, jsonify, request

from .config import config, db, guard, cors
from .models import User as UserModel


def create_app():
    """
    Creates a new Flask app using the configuration defined in
    config.py. The database is also initialized here (avoiding a
    circular import).

    :return: None
    """
    application = Flask(__name__)
    application.config.from_object(config["development"])

    guard.init_app(application, UserModel)
    db.init_app(application)
    cors.init_app(application)

    return app


app = create_app()


@app.route("/")
def home():
    return "Hello"


@app.route('/login', methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user
    credentials and issuing a JWT token.

    example:
    $ curl http://localhost:5000/login -X POST \
      -d '{"username":"user","password":"pwd"}'

    :return: access token if authentication succeeds
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)

    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}

    return jsonify(ret), 200


@app.route("/refresh", methods=["POST"])
def refresh():
    """
    Refreshes client token after expiry.

    :return: a new client token
    """
    req = request.get_json(force=True)
    ret = {'access_token': guard.refresh_jwt_token(req['token'])}
    return jsonify(ret), 200
