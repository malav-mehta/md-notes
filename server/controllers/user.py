"""
controllers/user.py

Controller for the User model.
"""
from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.config import db
from server.models import User as UserModel


class User(Resource):
    """
    Create a controller for handling requests to the Folders
    endpoint.

    URI:     /folders
    Methods: GET, POST
    """
    method_decorators = [auth_required]