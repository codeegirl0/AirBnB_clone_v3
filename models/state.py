#!/usr/bin/python3
"""
State Class 
"""
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from models.base_model import BaseModel, Base
import models
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """get app state"""
    if storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='delete')
    else:
        name = ''
    if storage_type != 'db':
        @property
        def cities(self):
            """
            getting method
            """
            city_list = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
