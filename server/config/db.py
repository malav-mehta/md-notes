"""
db.py

Database initialization occurs separately to avoid a circular import
with the applications's database models.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    """
    The setup for the database which creates the database tables
    with SQL Alchemy.

    :param app: the flask application
    :return: None
    """
    with app.app_context():
        db.create_all()
