#!/usr/bin/env python3
"""
Create a class BasicAuth that inherits from Auth
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                                str) -> str:
        """
        Extract base64 authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """
        Decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("utf-8")
        except Exception:
            return None
