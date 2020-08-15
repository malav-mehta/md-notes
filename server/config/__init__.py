"""
config

Application configuration and initialization of database, guard and
cors decentralized from ~/app.py.
"""

from .config import config
from .api import api
from .db import db, setup_db
from .guard import guard
from .cors import cors
