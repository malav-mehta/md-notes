"""
models/image.py

Create an Image model.
"""
from server.config import db


class Image(db.Model):
    # alias: image
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"))
    src = db.Column(db.String)
    delete_url = db.Column(db.String)

    def __repr__(self):
        return "<Image: {}, user: {}, note: {}, src: {}>".format(self.id, self.user_id, self.note_id, self.src)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
