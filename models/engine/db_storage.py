#!/usr/bin/python3
""" Database engine """

import os
from sqlalchemy import create_engine, MetaData
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """take storage for ints"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'State': state.State,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'User': user.User
    }

    """ handling db  """
    __engine = None
    __session = None

    def __init__(self):
        """ creating the engine self.__engine """

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ get a dictionary for objs """
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
            return obj_dict
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.CNC.get(class_name)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """ adding objs to db"""
        self.__session.add(obj)

    def get(self, cls, id):
        """
        fetches some object
        :param cls: class  object 
        :param id: id  object
        :return: object or None
        """
        all_class = self.all(cls)
        for obj in all_class.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """
        :param cls: the class name
        :return: take instc of a class
        """
        return len(self.all(cls))

    def save(self):
        """ take db changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """ remove obj from  database """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reload db """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
            calling remove() 
        """
        self.__session.remove()
