#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from api.model.tle_fetcher import Satellite, Base
from dotenv import load_dotenv
import os

load_dotenv()


class DBStorage:
    """interacts with the MySQL database"""
    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('SAT_MYSQL_USER'),
                                             os.getenv('SAT_MYSQL_PWD'),
                                             os.getenv('SAT_MYSQL_HOST'),
                                             os.getenv('SAT_MYSQL_DB')))

    def get_sat(self, name):
        """Get satellite by name"""
        return (self.__session.query(Satellite).filter_by(name=name).first())

    def new_sat(self, obj):
        """store new satellites"""
        self.__session.add(obj)

    def reload(self):
        """reload the database"""
        # reload all tables related to the database
        Base.metadata.create_all(self.__engine)
        # create session factory
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        # assign session to instance variable
        self.__session = Session

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
