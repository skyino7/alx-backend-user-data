#!/usr/bin/env python3
"""Auth module"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth method"""
        if path is None or not excluded_paths:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path.rstrip('*')):
                    return False
                elif path == excluded_path.rstrip('/'):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header method"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method"""
        return None
