"""
config/guard.py

Initializes a Praetorian guard for enabling and enforcing
authorization in the API.
"""
from flask_praetorian import Praetorian

guard = Praetorian()
