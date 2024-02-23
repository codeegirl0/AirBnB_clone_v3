#!/usr/bin/python3
"""
BaseModel the Class 
"""

import os
import json
import models
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime


storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
    Creating base instance 
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
        attr and funcs 
    """
    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """start of new BaseModel Class"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def serialing(self, obj_v):
        """
            prive: checking obj 
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, name, value):
        """
            updating the basemodel
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """updating attr """
        if storage_type != 'db':
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """get json self"""
        bm_dict = {}
        for key, value in (self.__dict__).items():
            if (self.serialing(value)):
                bm_dict[key] = value
            else:
                bm_dict[key] = str(value)
        bm_dict['__class__'] = type(self).__name__
        if '_sa_instance_state' in bm_dict:
            bm_dict.pop('_sa_instance_state')
        if storage_type == "db" and 'password' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """get type string """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
            remove  instance 
        """
        self.delete()
