from datetime import datetime
from typing import Any
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.mariadb.account import Account

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class Funding(Base, BaseModel):
    __tablename__ = 'funding'
    funding = Column(String)
    drawing = Column(String)
    acc_id = Column(String, ForeignKey(Account.acc_id))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, **entries):
        self.__dict__.update(entries)
