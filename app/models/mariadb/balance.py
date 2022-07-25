from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.mariadb.account import Account
from models.mariadb.order import Order

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class Balance(Base, BaseModel):
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String)
    balance = Column(String)
    locked = Column(String)
    avg_buy_price = Column(String)
    avg_buy_price_modified = Column(Integer)
    unit_currency = Column(String)
    created_at = Column(DateTime)
    order_uuid = Column(String, ForeignKey(Order.uuid))
    acc_id = Column(String, ForeignKey(Account.acc_id))

    def __init__(self, **entries):
        self.__dict__.update(entries)
