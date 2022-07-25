from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models.mariadb.order import Order

from models.mariadb.base_model import BaseModel
Base = declarative_base()

class Trade(Base, BaseModel):
    __tablename__ = 'trade'
    
    uuid = Column(String, primary_key=True)
    market = Column(String)
    price = Column(String)
    volume = Column(String)
    funds = Column(String)
    created_at = Column(DateTime)
    side = Column(String)
    trend = Column(String)
    order_uuid = Column(String, ForeignKey(Order.uuid))

    def __init__(self, **entries):
        self.__dict__.update(entries)
