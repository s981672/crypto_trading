

import apis.upbit.order_api as upbitOrder
import apis.binance.order_api as binanceOrder
from model.order_model import OrderModel


class OrderService():

    @staticmethod
    def order(orderInfo):
        """
        Webhook을 통해 주문 시그널이 수신된 경우.
        """
        api = upbitOrder.OrderApi()
        
        #TODO : 주문 정보를 별도로 가지고 오는 부분이 필요함.
        orderModel = OrderModel(
            price=6000,
            market='KRW-BTC',
            side='bid',
            type='price',
            id='BML_BUY_0000001'
        )
        return api.buy(param=orderModel)
        

    @staticmethod
    def order_chance(market: str):
        api = upbitOrder.OrderApi()
        return api.orders_chance(market=market)