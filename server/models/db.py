"""
db.py

Database initialization occurs separately to avoid a circular import
with the applications's database models.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
