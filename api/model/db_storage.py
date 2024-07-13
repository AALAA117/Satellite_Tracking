#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from api.model.tle_fetcher import Satellite, Base

class DBStorage:
    """interaacts with the MySQL database"""
    SAT_MYSQL_USER = 'sat_track'
    HBNB_MYSQL_PWD = 'sat_track_pwd'
    HBNB_MYSQL_HOST = 'localhost'
    HBNB_MYSQL_DB = 'sat_track_db'
    self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(SAT_MYSQL_USER,
                                             SAT_MYSQL_PWD,
                                             SAT_MYSQL_HOST,
                                             SAT_MYSQL_DB))
    def get_sat(self, name):
        """Get satellite by name"""
        return (session.query(Satellite).filter_by(name=name).first())
    
    def new_sat(self, obj):
        """store new satellites"""
        self.__session.add(obj)

    def reload(self):
        """reload the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()



