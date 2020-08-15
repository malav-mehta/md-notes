"""
models

Setup for the application's database models.
"""

# the database
from .db import db

# database models
from .folder import Folder
from .note import Note
from .image import Image
from .user import User
