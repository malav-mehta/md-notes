"""
models/user.py

Create a User table.
"""
import datetime
from passlib.hash import sha256_crypt

from . import db


class User(db.Model):
    # alias: user
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    open_folder_id = db.Column(db.Integer, db.ForeignKey("folder.id"), default=None)
    open_note_id = db.Column(db.Integer, db.ForeignKey("note.id"), default=None)

    @property
    def password(self):
        """
        Prevent password from begin accessed.
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password.

        :param password: the new password.
        """
        self.password_hash = sha256_crypt.encrypt(password)

    def verify_password(self, password):
        """
        Check if hashed password matches inputted password.

        :param password: the password to check.
        :return: whether the passwords match (boolean)
        """

        return sha256_crypt.verify(password, self.password_hash)

    def __repr__(self):
        return "<User: {}, name: {}, email: {}".format(self.id, self.username, self.email)
