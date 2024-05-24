#!/usr/bin/env python3
"""
Create a class SessionDBAuth
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for session
    authentication with database storage
    """

    def create_session(self, user_id=None):
        """
        Create and store a new instance of
        UserSession and return the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the User ID by requesting
        UserSession in the database based on session_id
        """
        if session_id is None:
            return None
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) == 0:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the
        Session ID from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) == 0:
            return False
        sessions[0].remove()
        return True
