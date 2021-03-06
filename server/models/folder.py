"""
models/folder.py

Create a Folder table.
"""
from server.config import db


class Folder(db.Model):
    # alias: folder
    __tablename__ = "folder"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(60))

    def __repr__(self):
        return "<Folder: {}, name: {}, owner: {}>".format(self.id, self.name, self.user_id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
