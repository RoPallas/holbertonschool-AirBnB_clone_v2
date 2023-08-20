#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.state import State
import os


class DBStorage():
    __engine = None
    __session = None

    def __init__(self):
        from models.base_model import Base
        username = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        if host == 'here':
            host = 'localhost'
        db_name = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            username,
            password,
            host,
            db_name
        ), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        objects = {}
        if cls is not None:
            for instance in self.__session.query(cls):
                objects[cls.__name__ + '.' + instance.id] = instance
            return objects
        else:
            classes = ["Amenity", "City", "Place", "Review", "State", "User"]
            for i in classes:
                for instance in self.__session(i):
                    objects[i + '.' + instance.id] = instance
            return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import Base
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from models.user import User

        Base.metadata.create_all(self.__engine)
        session_creation = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_creation)
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()