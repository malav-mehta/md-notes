"""
app.py

Initializes the application with the configuration and constructs the
RESTful API endpoints using the controllers.
"""
import datetime

from flask import Flask, jsonify, request
from flask_praetorian import auth_required, current_user

from .config import config
from .config import api
from .config import cors
from .config import db
from .config import guard

from .models import User as UserModel

from .controllers import Folders as FoldersController, Folder as FolderController
from .controllers import Images as ImagesController, ImagesByNote as ImagesByNoteController, Image as ImageController
from .controllers import Notes as NotesController, NotesByFolder as NotesByFolderController, NotesInTrash as Trash, Note as NoteController
from .controllers import Users as UsersController, User as UserController


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

    api.add_resource(FoldersController, "/folders")
    api.add_resource(FolderController, "/folder/<int:folder_id>")

    api.add_resource(ImagesController, "/images")
    api.add_resource(ImagesByNoteController, "/images/<int:note_id>")
    api.add_resource(ImageController, "/image/<int:image_id>")

    api.add_resource(Trash, "/trash")
    api.add_resource(NotesController, "/notes")
    api.add_resource(NotesByFolderController, "/notes/<int:folder_id>")
    api.add_resource(NoteController, "/note/<int:note_id>")

    api.add_resource(UsersController, "/users")
    api.add_resource(UserController, "/user")

    api.init_app(application)
    return application


app = create_app()


@app.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user
    credentials and issuing a JWT token.

    example:
    $ curl http://localhost:5000/login -X POST \
      -d "{"username":"user","password":"pwd"}"

    :return: access token if authentication succeeds
    """
    req = request.get_json(force=True)
    username = req.get("username", None)
    password = req.get("password", None)

    user = guard.authenticate(username, password)
    user.last_login = datetime.datetime.utcnow()
    db.session.commit()

    ret = {
        "data": {
            "access_token": guard.encode_jwt_token(user),
            "user": user.as_dict()
        },
        "error": None,
        "message": "OK",
        "status_code": 200,
    }

    return jsonify(ret), 200


@app.route("/refresh", methods=["POST"])
def refresh():
    """
    Refreshes client token after expiry.

    :return: a new client token
    """
    req = request.get_json(force=True)
    ret = {"access_token": guard.refresh_jwt_token(req["token"])}
    return jsonify(ret), 200
