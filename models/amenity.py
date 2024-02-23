#!/usr/bin/python3
"""
Amenity Class 
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """ handling all app """
    if storage_type == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
    else:
        name = ''
