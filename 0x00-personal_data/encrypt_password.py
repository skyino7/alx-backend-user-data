#!/usr/bin/env python3
"""
mplement a hash_password function that
expects one string argument name password
and returns a salted, hashed password,
which is a byte string
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and
    returns the salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password
    matches the hashed password.
    """
    check = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return check
