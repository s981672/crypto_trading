

from typing import List
from pydantic import BaseModel


class OrderBookUnit(BaseModel):
    ask_price: float
    bid_price: float
    ask_size: float
    bid_size: float
    

class OrderBookData(BaseModel):
    market: str
    timestamp: float
    total_ask_size: float
    total_bid_size: float
    orderbook_units: List[OrderBookUnit]
    

class OrderBook(BaseModel):
    created_at: str
    order_book: List[OrderBookData]
    