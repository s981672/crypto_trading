from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.mariadb.account import Account
from models.mariadb.algorithm import Algorithm

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class Order(Base, BaseModel):
    __tablename__ = 'orders'
    
    uuid = Column(String, primary_key=True)
    side = Column(String)
    ord_type = Column(String)
    price = Column(String)
    state = Column(String)
    reserved_fee = Column(String)
    remaining_fee = Column(String)
    paid_fee = Column(String)
    locked = Column(String)
    executed_volume = Column(String)
    trades_count = Column(Integer)
    volume = Column(String)
    remaining_volume = Column(String)
    market = Column(String)
    algorithm_id = Column(String, ForeignKey(Algorithm.algorithm_id))
    acc_id = Column(String, ForeignKey(Account.acc_id))
    trades_count = Column(Integer)
    
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def to_dict(self):
        return {
            "uuid" : self.uuid,
            "side" : self.side,
            "ord_type" : self.ord_type,
            "price" : self.price,
            "state" : self.state,
            "reserved_fee" : self.reserved_fee,
            "remaining_fee" : self.remaining_fee,
            "paid_fee" : self.paid_fee,
            "locked" : self.locked,
            "executed_volume" : self.executed_volume,
            "trades_count" : self.trades_count,
            "volume" : self.volume,
            "market" : self.market,
            "remaining_fee" : self.remaining_fee,
            "algorithm_id" : self.algorithm_id,
            "acc_id" : self.acc_id,
            "trades_count" : self.trades_count,
        }