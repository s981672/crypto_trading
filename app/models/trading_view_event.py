
from pydantic import BaseModel


class TradingViewEvent(BaseModel):
    strategy_id : str
    ticker : str
    order_id : str
    action : str
    contracts : str
    price : str
    position_size : str