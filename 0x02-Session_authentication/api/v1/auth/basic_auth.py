#!/usr/bin/env python3
"""
Create a class BasicAuth that inherits from Auth
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User


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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """Extract User Credentials"""
        decoded = decoded_base64_authorization_header
        if decoded is None:
            return None, None
        if type(decoded) is not str:
            return None, None
        if ":" not in decoded:
            return None, None
        user_email, user_pwd = decoded.split(":", 1)
        return user_email, user_pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> 'User':
        """User Object From Credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> 'User':
        """Current User"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        email, pwd = self.extract_user_credentials(decoded_header)

        return self.user_object_from_credentials(email, pwd)
