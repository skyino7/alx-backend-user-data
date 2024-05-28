#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Returns a User object
        """
        try:
            add_user = User(email=email, hashed_password=hashed_password)
            session = self._session
            session.add(add_user)
            session.commit()
        except Exception:
            session.rollback()
            add_user = None
        return add_user

    def find_user_by(self, **kwargs: dict) -> User:
        """find a user based on the keywords args and return
            the first row
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        method that takes as argument a required
        user_id integer and arbitrary keyword arguments,
        and returns None
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update = {}
        for key, value in kwargs.items():
            if key not in User.__table__.columns:
                raise ValueError
            update[key] = value
        session.query(User).filter_by(id=user_id).update(update)
        session.commit()
