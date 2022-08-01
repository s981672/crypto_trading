from datetime import datetime
from typing import Any
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.mariadb.account import Account
from models.mariadb.algorithm import Algorithm

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class AlgorithmList(Base, BaseModel):
    __tablename__ = 'algorithm_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm_id = Column(String, ForeignKey(Algorithm.algorithm_id))
    acc_id = Column(String, ForeignKey(Account.acc_id))
    sub_algorithm_id = Column(String)
    initial_money = Column(String)
    total_money = Column(String)
    current_division = Column(Integer)
    executed_volume = Column(String)
    working = Column(Boolean)
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
