#!/usr/bin/env python3
"""
Create a class SessionExpAuth
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for session
    authentication with expiration
    """

    def __init__(self):
        """
        Initialize session duration
        """
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create session with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_data = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve user ID with session
        expiration check
        """
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data.get('user_id')
        created_at = session_data.get('created_at')
        if created_at is None:
            return None
        if created_at + timedelta(
                                seconds=self.session_duration
                            ) < datetime.now():
            return None
        return session_data.get('user_id')
