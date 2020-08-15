"""
models/user.py

Create a User table.
"""
import datetime

from server.config import db
from server.config import guard


class User(db.Model):
    # alias: user
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    open_folder_id = db.Column(db.Integer, db.ForeignKey("folder.id"), default=None)
    open_note_id = db.Column(db.Integer, db.ForeignKey("note.id"), default=None)

    @property
    def rolenames(self):
        """
        Required for Flask-Praetorian

        :return: None
        """
        return []

    @classmethod
    def lookup(cls, username):
        """
        Looks up a user in the table.

        :param username: the looked-up user's username
        :return: the user or None if the user wasn't found
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        Returns a user based on the given id.

        :param id: the id of the user
        :return: the user with the given id
        """
        return cls.query.get(id)

    @property
    def identity(self):
        """
        Required for Flask-Praetorian.

        :return: the id of the user
        """
        return self.id

    def is_valid(self):
        """
        Required for Flask-Praetorian

        :return: whether the user token is active
        """
        return self.is_active

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<User: {}, name: {}, email: {}>".format(self.id, self.username, self.email)
