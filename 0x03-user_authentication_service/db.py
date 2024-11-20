#!/usr/bin/env python3
"""
DB module.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from user import Base, User


class DB:
    """
    DB class.
    """

    def __init__(self):
        """
        initialize a new DB instance
        """

        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        Add new user to db

        Args:
            email: user email
            hashed_password: user password
        Returns:
            User: new user object
        """

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Get user by key-value pair
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found")
        except MultipleResultsFound:
            raise InvalidRequestError("Multiple users found")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database.

        Args:
        - user_id (int): The ID of the user to update.
        - **kwargs: Keyword arguments for the attributes to update.

        Returns:
        - None
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            raise ValueError("User not found")

        for key, value in kwargs.items():
            if key not in ["email", "hashed_password", "session_id", "reset_token"]:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
