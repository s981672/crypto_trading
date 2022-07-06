
from apis.abstract_api import AbstractOrder


class OrderApi(AbstractOrder):
    
    def order(self, param):
        print('Binance Order')