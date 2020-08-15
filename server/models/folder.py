"""
models/folder.py

Create a Folder table.
"""
from . import db


class Folder:
    # alias: folder
    __tablename__ = "folder"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(60))

    def __repr__(self):
        return "<Folder: {}, name: {}, owner: {}>".format(self.id, self.name, self.user_id)
