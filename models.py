"""models.py: Creates ORM objects for 'OTR Program Catalog' app."""

from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
import random
import string
import datetime
from validation_routines import strIsInt, strLenValid, strIntValid
from db_creds import db_creds

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits
                                   ) for x in range(32))


class User(Base):
    """
    Class for User table, which stores application user records.

    Attributes:
        id (Integer): Primary key
        username (String): User's name
        picture (String): URL pointing to user's picture
        email (String): User's email address
        time_created (DateTime): Record creation timestamp
        time_updated (DateTime): Record update timestamp
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, index=True)
    picture = Column(String)
    email = Column(String, unique=True, nullable=False, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.username,
            'id': self.id,
            'picture': self.picture,
            'email': self.email
        }


class Genre(Base):
    """
    Class for Genre table which stores the app's genre records.

    Genre records contain information about Old Time Radio genres or
    categories (e.g., Comedy, Western, etc.) entered by users.

    Attributes:
        id (Integer): Primary key
        name (String): Genre name (e.g., Comedy)
        user_id (Integer): Id of user who added the genre
            (Foreign key pointing to "id" field in User table)
        user (Relationship): Link to User class
        time_created (DateTime): Record creation timestamp
        time_updated (DateTime): Record update timestamp
    """
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @validates('name')
    def validate_name(self, key, name):
        """Validator routine for genre 'name' field."""
        name = name.strip()
        if not name or name == '':
            raise AssertionError('Genre name missing.')
        if not strLenValid(name, 1, 100):
            raise AssertionError('Genre name must be between 1 and 100 \
                                 characters in length.')
        return name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


class Program(Base):
    """
    Class for Program table which stores the app's program records.

    Program records contain information about specific Old Time Radio
    programs entered by users.

    Attributes:
        id (Integer): Primary key
        name (String): Program name (e.g., The Lone Ranger)
        description (String): Description of program
        yearBegan (Integer): Year the program was first broadcast
        yearEnded (Integer): Year the program was last broadcast
        genre_id (Integer): Id of genre to which program belongs
            (Foreign key pointing to "id" field in Genre table)
        genre (relationship): Link to Genre class
        user_id (Integer): Id of user who added the program
            (Foreign key pointing to "id" field in User table)
        user (Relationship): Link to User class
        time_created (DateTime): Record creation timestamp
        time_updated (DateTime): Record update timestamp
    """
    __tablename__ = 'program'
    name = Column(String(120), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    yearBegan = Column(Integer, nullable=False)
    yearEnded = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @validates('name')
    def validate_name(self, key, name):
        """Validator routine for program 'name' field."""
        name = name.strip()
        if not name or name == '':
            raise AssertionError('Program name missing.')
        if not strLenValid(name, 1, 120):
            raise AssertionError('Program name must be between 1 and 120 \
                                 characters in length.')
        return name

    # The following method validates both yearBegan and yearEnded fields,
    # applying the same requirements except in the case of yearEnded, which
    # adds logic to ensure yearEnded is greater than or equal to yearBegan.
    @validates('yearBegan', 'yearEnded')
    def validate_yearEndedGTEyearBegan(self, key, value):
        """Validator routine for 'yearBegan' and 'yearEnded' fields."""
        value = value.strip()
        if not value or value == '':
            raise AssertionError('{} missing.'.format(key))
        if not strIsInt(value) or not strIntValid(value, 1920, 1980):
            raise AssertionError('{} must be an integer year between 1920 \
                                 and 1980.'.format(key))
        if key == 'yearEnded' and not self.yearBegan <= value:
            raise AssertionError('yearEnded must be greater than or equal \
                                 to yearBegan.')
        return value

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'yearBegan': self.yearBegan,
            'yearEnded': self.yearEnded,
            'genre_id': self.genre_id
        }


# Connect to Database and create database session.
dbURL = "{}://{}:{}@{}:{}/{}".format(
                                     db_creds['driver'],
                                     db_creds['user'],
                                     db_creds['passwd'],
                                     db_creds['host'],
                                     db_creds['port'],
                                     db_creds['database'])
engine = create_engine(dbURL)
Base.metadata.create_all(engine)
