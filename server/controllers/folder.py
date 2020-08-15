"""
controllers/folder.py

Controller for the Folder model.
"""
from flask_praetorian import auth_required, current_user
from flask_restful import Resource

from server.models import Folder as FolderModel


class Folder(Resource):
    """
    Create a controller for handling requests to the Folder endpoint,
    with URIs:

    GET     /folder/<int:folder_id>
    PUT     /folder/<int:folder_id>
    DELETE  /folder/<int:folder_id>
    """
    method_decorators = [auth_required]

    def get(self, folder_id):

