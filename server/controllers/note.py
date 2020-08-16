"""
controllers/note.py

Controller for the Note model.
"""
from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.config import db
from server.models import Folder as FolderModel
from server.models import Note as NoteModel
from server.util import is_int


class Notes(Resource):
    """
    Create a controller for handling requests to the Notes endpoint.

    URI:     /notes
    Methods: GET, POST
    """
    method_decorators = [auth_required]

    def get(self):
        notes = [note.as_dict() for note in NoteModel.query.filter_by(user_id=current_user().id).all()]

        for note in notes:
            del note["content"]

        return jsonify({
            "data": notes,
            "error": None,
            "message": "OK",
            "status_code": 200,
        })

    def post(self):
        payload = request.get_json(force=True)
        errors = {}

        folder_id = payload.get("folder_id", None)
        title = payload.get("title", None)
        body = payload.get("body", None)

        if not folder_id or not is_int(folder_id) or not FolderModel.query.filter_by(id=int(folder_id),
                                                                                     user_id=current_user().id).one_or_none():
            errors["folder_id"] = "The folder id is invalid."

        if not title:
            errors["title"] = "The title is a required argument."

        elif not len(title) < 60:
            errors["title"] = "The title must be less than 60 characters long."

        if not body:
            body = ""

        if errors:
            return jsonify({
                "data": None,
                "error": errors,
                "message": "The required parameters were not fulfilled.",
                "status_code": 400,
            })

        else:
            note = NoteModel(user_id=current_user().id, folder_id=folder_id, title=title, body=body)
            db.session.add(note)
            db.session.commit()

            return jsonify({
                "data": note.as_dict(),
                "error": None,
                "message": "OK",
                "status_code": 201,
            })


class NotesByFolder(Resource):
    """
        Create a controller for handling requests to the Notes endpoint.

        URI:     /notes/<int:folder_id>
        Methods: GET, POST
        """
    method_decorators = [auth_required]

    def get(self, folder_id):
        if FolderModel.query.filter_by(id=folder_id, user_id=current_user().id).one_or_none():
            notes = [note.as_dict() for note in
                     NoteModel.query.filter_by(folder_id=folder_id, user_id=current_user().id).all()]

            for note in notes:
                del note["content"]

            return jsonify({
                "data": notes,
                "error": None,
                "message": "OK",
                "status_code": 200,
            })

        else:
            return jsonify({
                "data": None,
                "error": "NotFoundError",
                "message": "Resource not found.",
                "status_code": 404,
            })


class Note(Resource):
    """
    Create a controller for handling requests to the Note endpoint.

    URI:     /note/<int:note_id>
    Methods: GET, PUT, DELETE
    """
    method_decorators = [auth_required]
