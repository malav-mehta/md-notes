"""
controllers/folder.py

Controller for the Folder model.
"""
from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.config import db
from server.models import Folder as FolderModel


class Folders(Resource):
    """
    Create a controller for handling requests to the Folders
    endpoint.

    URI:     /folders
    Methods: GET, POST
    """
    method_decorators = [auth_required]

    def get(self):
        folders = [folder.as_dict() for folder in FolderModel.query.filter_by(user_id=current_user().id).all()]

        return jsonify({
            "data": folders,
            "error": None,
            "message": "OK",
            "status_code": 200,
        })

    def post(self):
        payload = request.get_json(force=True)
        errors = {}

        name = payload.get("name", None)

        if not name:
            errors["name"] = "The new folder name is a required argument."

        elif len(name) > 60:
            errors["name"] = "The new folder name must be 60 characters long."

        if errors:
            return jsonify({
                "data": None,
                "error": errors,
                "message": "The required parameters were not fulfilled.",
                "status_code": 400,
            })

        else:
            folder = Folder(name=name)
            db.session.add(folder)
            db.session.commit()

            return jsonify({
                "data": folder.as_dict(),
                "error": None,
                "message": "OK",
                "status_code": 201,
            })


class Folder(Resource):
    """
    Create a controller for handling requests to the Folder endpoint.

    URI:     /folder/<int:folder_id>
    Methods: GET, PUT, DELETE
    """
    method_decorators = [auth_required]

    def get(self, folder_id):
        folder = FolderModel.query.filter_by(id=folder_id, user_id=current_user().id).one_or_none()

        if folder:
            return jsonify({
                "data": folder.as_dict(),
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

    def put(self, folder_id):
        folder = FolderModel.query.filter_by(id=folder_id, user_id=current_user().id).one_or_none()

        if folder:
            payload = request.get_json(force=True)
            errors = {}

            name = payload.get("name", None)
            
            if not name:
                errors["name"] = "The new folder name is a required argument."

            elif len(name) > 60:
                errors["name"] = "The new folder name must be 60 characters long."

            else:
                folder.name = name
                db.session.commit()

            if errors:
                return jsonify({
                    "data": folder.as_dict(),
                    "error": errors,
                    "message": "The required parameters were not fulfilled.",
                    "status_code": 400,
                })

            return jsonify({
                "data": folder.as_dict(),
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

    def delete(self, folder_id):
        folder = FolderModel.query.filter_by(id=folder_id, user_id=current_user().id).one_or_none()

        if folder:
            db.session.delete(folder)
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
