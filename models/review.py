#!/usr/bin/python3
"""
Review Class from Models Module
"""
import os
from sqlalchemy import Column, Integer, String, Float, ForeignKey
storage_type = os.environ.get('HBNB_TYPE_STORAGE')
from models.base_model import BaseModel, Base



class Review(BaseModel, Base):
    """get  application rvw"""
    if storage_type == "db":
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ''
        user_id = ''
        text = ''