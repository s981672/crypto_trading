from abc import *

from model.order_model import OrderModel

class AbstractOrder(metaclass=ABCMeta):
    
    @abstractmethod
    def order(self, param: OrderModel):
        pass
    
    def buy(self, param: OrderModel):
        pass
    
    def orders_chance(self, market: str):
        pass
    
class AbstractAccount(metaclass=ABCMeta):
    
    @abstractmethod
    def account(self):
        pass
    