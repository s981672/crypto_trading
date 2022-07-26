
import re
from typing import Any
from pydantic import BaseModel
from regex import F


class TradingViewEvent(BaseModel):
    strategy_id : str
    ticker : str
    order_id : str
    action : str
    contracts : str
    price : str
    position_size : str
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        # order id 값이 'Close Entry(s) order L[1]' 형태로 올 수도 있기에 정규식을 사용하여 ID를 추출함.
        regex = re.compile(r'[LS]\[[0-9]\]')
        order_id = regex.search(data['order_id'])
        data['order_id'] = order_id.group()

        super().__init__(**data)