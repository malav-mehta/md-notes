"""
controllers/image.py

Controller for the Image model.
"""
from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.config import db

from server.util import is_int

from server.models import Image as ImageModel
from server.models import Note as NoteModel


class Images(Resource):
    """
    Create a controller for handling requests to the Images endpoint.

    URI:     /images
    Methods: GET, POST
    """
    method_decorators = [auth_required]

    def get(self):
        images = [image.as_dict() for image in ImageModel.query.filter_by(user_id=current_user().id).all()]

        return jsonify({
            "data": images,
            "error": None,
            "message": "OK",
            "status_code": 200,
        })

    def post(self):
        payload = request.get_json(force=True)
        errors = {}

        note_id = payload.get("note_id", None)
        src = payload.get("src", None)
        delete_url = payload.get("delete_url", None)

        if not note_id or not is_int(note_id) or not NoteModel.query.filter_by(id=int(note_id), user_id=current_user().id).one_or_none():
            errors["note_id"] = "The note id is invalid."

        if not src:
            errors["src"] = "An src for the image must be defined."

        if not delete_url:
            errors["delete_url"] = "A delete_url for the image must be defined."

        if errors:
            return jsonify({
                "data": None,
                "error": errors,
                "message": "The required parameters were not fulfilled.",
                "status_code": 400,
            })

        else:
            image = ImageModel(user_id=current_user().id, note_id=note_id, src=src, delete_url=delete_url)
            db.session.add(image)
            db.session.commit()

            return jsonify({
                "data": image.as_dict(),
                "error": None,
                "message": "OK",
                "status_code": 201,
            })


class Image(Resource):
    """
    Create a controller for handling requests to the Image endpoint.

    URI:     /image/<int:image_id>
    Methods: GET, PUT, DELETE
    """
    method_decorators = [auth_required]

    def get(self, image_id):
        image = ImageModel.query.filter_by(id=image_id, user_id=current_user().id).one_or_none()

        if image:
            return jsonify({
                "data": image.as_dict(),
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

    def put(self, image_id):
        image = ImageModel.query.filter_by(id=image_id, user_id=current_user().id).one_or_none()

        if image:
            payload = request.get_json(force=True)
            errors = {}

            note_id = payload.get("note_id", None)
            src = payload.get("src", None)
            delete_url = payload.get("delete_url", None)

            if not note_id or not is_int(note_id) or not NoteModel.query.filter_by(id=int(note_id), user_id=current_user().id).one_or_none():
                errors["note_id"] = "The note id is invalid."

            if not src:
                errors["src"] = "An src for the image must be defined."

            if not delete_url:
                errors["delete_url"] = "A delete_url for the image must be defined."

            if errors:
                return jsonify({
                    "data": None,
                    "error": errors,
                    "message": "The required parameters were not fulfilled.",
                    "status_code": 400,
                })

            else:
                image.note_id = note_id
                image.src = src
                image.delete_url = delete_url
                db.session.commit()

            return jsonify({
                "data": image.as_dict(),
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

    def delete(self, image_id):
        image = ImageModel.query.filter_by(id=image_id, user_id=current_user().id).one_or_none()

        if image:
            db.session.delete(image)
            db.session.commit()

            return jsonify({
                "data": None,
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
