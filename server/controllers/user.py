"""
controllers/user.py

Controller for the User model.
"""
import re

from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.config import db
from server.config import guard

from server.models import User as UserModel


class Users(Resource):
    """
    Create a controller for handling requests to the Users endpoint.

    URI:     /users
    Methods: POST
    """

    def post(self):
        payload = request.get_json(force=True)
        errors = {}
        email_regex = re.compile("^[a-z0-9]+[. ]?[a-z0-9]+[@]\w+[.]\w+$")

        username = payload.get("username", None)
        email = payload.get("email", None)
        password = payload.get("password", None)

        if not username:
            errors["username"] = "Each user must have a username."

        elif not len(username) < 60:
            errors["username"] = "Your username must not exceed 60 characters."

        elif UserModel.query.filter_by(username=username).one_or_none():
            errors["username"] = "The username is taken."

        if not email:
            errors["email"] = "Each user must have an email."

        elif not len(email) < 60:
            errors["email"] = "Your email must not exceed 60 characters."

        elif not email_regex.fullmatch(email):
            errors['email'] = "The email is not in a valid format."

        if not password:
            errors["password"] = "You must enter a password."

        elif not 6 <= len(password) <= 60:
            errors["password"] = "Your password must be 6 to 60 characters long."

        if errors:
            return jsonify({
                "data": None,
                "error": errors,
                "message": "The required parameters were not fulfilled.",
                "status_code": 400,
            })

        user = UserModel(username=username, email=email, password=guard.hash_password(password))
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "data": user.as_dict(),
            "error": None,
            "message": "OK",
            "status_code": 201,
        })


class User(Resource):
    """
    Create a controller for handling requests to the User endpoints.

    URI:     /user
    Methods: GET, PUT
    """
    method_decorators = [auth_required]

    def get(self):
        return jsonify({
            "data": current_user().as_dict(),
            "error": None,
            "message": "OK",
            "status_code": 200,
        })

    def put(self):
        payload = request.get_json(force=True)
        errors = {}
        email_regex = re.compile("^[a-z0-9]+[. ]?[a-z0-9]+[@]\w+[.]\w+$")

        username = payload.get("username", None)
        email = payload.get("email", None)
        password = payload.get("password", None)

        if username:
            if not len(username) < 60:
                errors["username"] = "Your username must not exceed 60 characters."

            elif UserModel.query.filter_by(username=username).one_or_none():
                errors["username"] = "The username is taken."

        if email:
            if not len(email) < 60:
                errors["email"] = "Your email must not exceed 60 characters."

            elif not email_regex.fullmatch(email):
                errors['email'] = "The email is not in a valid format."

        if password and not 6 <= len(password) <= 60:
            errors["password"] = "Your password must be 6 to 60 characters long."

        if errors:
            return jsonify({
                "data": None,
                "error": errors,
                "message": "The required parameters were not fulfilled.",
                "status_code": 400,
            })

        if username:
            current_user().username = username

        if email:
            current_user().email = email

        if password:
            current_user().password = guard.hash_password(password)

        db.session.commit()

        return jsonify({
            "data": current_user().as_dict(),
            "error": None,
            "message": "OK",
            "status_code": 201,
        })
