"""
models/note.py

Create a Note table.
"""
import datetime

from . import db


class Note(db.model):
    # alias: note
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    folder_id = db.Column(db.Integer, db.ForeignKey("folder.id"))
    in_trash = db.Column(db.Boolean, default=False)
    public_key = db.Column(db.String(60), default=None, nullable=True)
    title = db.Column(db.String(60))
    content = db.Column(db.UnicodeText)
    preview = db.Column(db.UnicodeText(60), default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def body(self):
        """
        Getter for the body of the note.

        :return: the body of the note.
        """
        return self.content

    @body.setter
    def body(self, body):
        """
        Setter for the body of the note, which also sets the preview
        text for the note.

        :param body: the new body of the note.
        """
        self.content = body
        self.preview = body[:60]

    def __repr__(self):
        return "<Note: {}, title: {}, author: {}>".format(self.id, self.title, self.user_id)
