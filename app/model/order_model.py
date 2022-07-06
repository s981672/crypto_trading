

from itsdangerous import json
from pydantic import BaseModel

from errors.exceptions import BadParameterException


class OrderModel(BaseModel):
    price: int = 0
    market: str = None
    side: str = None
    volume: int = 0
    type: str = None
    id: str = None
          
    def toJson(self):
        dict = {}
        if self.price > 0:
            dict['price'] = str(self.price)
        if self.volume > 0:
            dict['volume'] = str(self.volume)
        if self.id != None:
            dict['identifier'] = self.id
        dict['ord_type'] = self.type
        dict['side'] = self.side
        dict['market'] = self.market

        return dict
        
            
        
    
class ApiResponse(BaseModel):
    id: str = None
    side: str = None
    