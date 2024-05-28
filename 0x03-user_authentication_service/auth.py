#!/usr/bin/env python3
"""
Module for hashing passwords
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    """
    salted = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salted)
    return hashed
