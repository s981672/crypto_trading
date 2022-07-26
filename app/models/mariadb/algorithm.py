from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class Algorithm(Base, BaseModel):
    __tablename__ = 'algorithm'
    algorithm_id = Column(String, primary_key=True)
    type = Column(String)
    exchange = Column(String)
    market = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    max_division = Column(Integer)

    def __init__(self, **entries):
        self.__dict__.update(entries)
