
from datetime import datetime
from typing import List
from pydantic import BaseModel

class Trade(BaseModel):
    market : str
    uuid : str
    price : str
    volume : str
    funds : str
    created_at : str
    side : str

class OrderInfo(BaseModel):
    uuid : str
    side : str
    ord_type : str
    price : str = None
    state : str
    market : str
    created_at : str
    volume : str
    remaining_volume : str
    reserved_fee : str
    remaining_fee : str
    paid_fee : str
    locked : str
    executed_volume : str
    trades_count : int
    trades : List[Trade]
        

class Order(BaseModel):
    user_id : str
    uuid: str
    strategy_id : str
    created_at : str
    updated_at : str
    order : OrderInfo
    