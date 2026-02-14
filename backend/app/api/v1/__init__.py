"""
API v1 module initialization
"""
from app.api.v1 import patients, triage, hospitals, outbreak, admin, tokens

__all__ = ["patients", "triage", "hospitals", "outbreak", "admin", "tokens"]

