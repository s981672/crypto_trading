

from abc import ABCMeta, abstractclassmethod, abstractmethod
from datetime import datetime
from logging import Logger, log, warning
import logging
import time
from typing import Dict
from numpy import double

from pytz import timezone
from pusher.telegram import TelegramBot
from models.mariadb.balance import Balance
from models.mariadb.trade import Trade
from models.mariadb.order import Order
from models.mariadb.algorithm_list import AlgorithmList
from database.mariadb_handler import MariadbHandler
from models.trading_view_event import TradingViewEvent
import exchanges.main as ex

logger = logging.getLogger(__name__)

class BaseAlgorithm(metaclass=ABCMeta):
    def __init__(self, event:TradingViewEvent = None):
        self._db_handler = MariadbHandler()
        self._access = 'DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P'
        self._secret = 'fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt'
        self._event = event

    @abstractmethod
    def run_algorithm(self):
        pass

    def __calc_buy_price(self, algorithm_list:AlgorithmList):
        """
        주문이 가능한 금액을 계산한다.

        Args:
            algorithm_list (AlgorithmList): 알고리즘 리스트

        Returns:
            _type_: 주문이 가능한 금액
        """
        current_money = double(algorithm_list.total_money)
        
        # 수수료가 0.05% 이기 때문에 해당 금액이 계산되어 매수 금액이 측정 되어야 함.
        enable_money = current_money / 1.0005
        logger.info(f"# Enable Order Price: {enable_money}")
        return str(enable_money)
    
    def __calc_sell_volume(self, algorithm_list:AlgorithmList):
        current_volume = double(algorithm_list.executed_volume)
        logger.info(f"# Enable Sell Order Volume : {current_volume}")
        return str(current_volume)
    
    def buy(self, *, exchange:str, market:str, ord_type:str = "price", algorithm_list:AlgorithmList):
        
        """
        매수 요청.
        1. 지정된 금액을 기준으로 매수를 요청한다.
        2. 주문 완료 후 신규 order 정보를 db에 쌓는다.
        3. 주문 UUID를 기준으로 주문 정보를 조회한다.
        4. 주문이 완료가 되었으면 trade 정보를 db에 쌓는다.
        5. 주문 정보를 기반으로 algorithm_list의 데이터를 업데이트 한다.
        6. 계좌 정보를 요청하여 balance 정보를 db에 쌓는다.
        """
        
        # algorithm에 있는 값을 기반으로 현재 구매 가능한 금액을 얻어온다.
        price = self.__calc_buy_price(algorithm_list)

        print(f'Buy : exchange:{exchange}, market:{market}, price:{price}')
        
        # 1. 지정된 금액을 기준으로 매수 요청.
        res = ex.post_order(
            exchange=exchange, 
            access=self._access, 
            secret=self._secret, 
            market=market, 
            side='bid', 
            ord_type=ord_type,
            price=price)
               
        # 2. order db에 추가
        order = self.__create_order_item(res, algorithm_list)
        
        # 3. 주문 정보 조회 및 업데이트.
        self.__update_order_info(exchange, order.uuid, algorithm_list)
        
        
        
    def sell(self, *, exchange:str, market:str, ord_type:str = "market", algorithm_list:AlgorithmList):
        """
        매도 요청.
        1. algorithm_list의 volume 값을 기준으로 매도를 요청한다.
        2. 주문 완료 후 신규 order 정보를 db에 쌓는다.
        3. 주문 UUID를 기준으로 주문 정보를 조회한다.
        4. 주문이 완료가 되었으면 trade 정보를 db에 쌓는다.
        5. 주문 정보를 기반으로 algorithm_list의 데이터를 업데이트 한다.
        6. 계좌 정보를 요청하여 balance 정보를 db에 쌓는다.
        """
        
        volume = self.__calc_sell_volume(algorithm_list)
        
        print(f'Sell : exchange:{exchange}, market:{market}, volume:{volume}')

        res = ex.post_order(
            exchange=exchange, 
            access=self._access, 
            secret=self._secret, 
            market=market, 
            side='ask', 
            ord_type=ord_type,
            volume=volume)
        
        # 2. order db에 추가
        order = self.__create_order_item(res, algorithm_list)
        
        # 3. 주문 정보 조회 및 업데이트.
        self.__update_order_info(exchange, order.uuid, algorithm_list)
        
    
    def __create_order_item(self, orderData:Dict, algorithm_list:AlgorithmList) -> Order:
        """
        주문 정보를 DB에 쌓는다.
        """
        
        if orderData is None or orderData['success'] is False:
            print(f'주문 실패 : {orderData}')
            return
        
        # 2. order db에 추가
        orderData = orderData['data']
        orderData['acc_id']=algorithm_list.acc_id
        orderData['algorithm_id']=algorithm_list.algorithm_id
        orderData['created_at']=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        order: Order = Order(**orderData)
        self._db_handler.insert_item(order)

        return order
        
    
    def __update_order_info(self, exchange:str, uuid:str, algorithm_list: AlgorithmList):
        
        check_completed = False
        
        while True:
            if check_completed is True:
                break

            res = ex.get_order_info(
                exchange=exchange,
                access=self._access,
                secret=self._secret,
                uuid=uuid,
                )
            
            print(res, res['success'], res['data']['state'])
            if res['success'] is True and (res['data']['state'] == "cancel" or res['data']['state'] == "done"):
                check_completed = True
                # Trade 정보를 DB에 쌓는다
                tradeData = res['data']['trades']
                print(f'### Trade: {tradeData}')
                for data in tradeData:
                    data['created_at'] = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
                    trade = Trade(**data)
                    trade.order_uuid = uuid
                    self._db_handler.insert_item(trade)

                # order 정보를 업데이트한다.
                orderData = res['data']
                orderData['acc_id']=algorithm_list.acc_id
                orderData['algorithm_id']=algorithm_list.algorithm_id
                orderData['created_at']=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
                orderData['updated_at']=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
                # del orderData['trades']
                order: Order = Order(**orderData)

                self._db_handler.update_item({'uuid':uuid}, order)
                
                # algorithm list를 업데이트 한다.
                self.__update_algorithm_list(orderData, algorithm_list)
                
                # balance를 조회한다.
                self.__get_balance_list(exchange, order.uuid, order.acc_id)
                
                # Telegram을 통해 메시지를 전송
                self.__send_message(order.side, 
                    self.__calc_funds(tradeData),
                    self.__calc_btc_price(tradeData),
                    res['data']['executed_volume'])

            else:
                time.sleep(1)



    def __update_algorithm_list(self, orderData:Dict, algorithm_list:AlgorithmList):
        (total_money, total_volume) = self.__calc_total_volume_and_price(orderData, algorithm_list)
        print(total_volume, total_money)
        algorithm_list.total_money = str(total_money)
        algorithm_list.executed_volume = str(total_volume)
        
        self._db_handler.update_item(
            {'algorithm_id':algorithm_list.algorithm_id,
             'sub_algorithm_id':algorithm_list.sub_algorithm_id},
            algorithm_list
            )
        
    def __calc_total_volume_and_price(self, orderData:Dict, algorithm_list:AlgorithmList):
        total_money = double(algorithm_list.total_money)
        total_volume = double(algorithm_list.executed_volume)
        
        side = orderData['side']
        tradeData = orderData['trades']

        # 수수료는 무조건 전체 금액에서 빠진다.
        total_money -= double(orderData['paid_fee'])
        
        for data in tradeData:
            # 주문인 경우에는 금액이 줄어들고 volume이 늘어난다.
            print(f"#### VOLUME : {data['volume']}")
            if side == 'bid':
                total_money -= double(data['funds'])
                total_volume += double(data['volume'])
            # 매도인  경우에는 금액이 늘어나고 volume이 줄어든다.
            else:
                total_money += double(data['funds'])
                total_volume -= double(data['volume'])

        return (total_money, total_volume)
            
    def __get_balance_list(self, exchange:str, order_uuid:str, acc_id:str):
        res = ex.get_accounts(
            exchange=exchange,
            access=self._access,
            secret=self._secret
        )
        
        if res is None or res['success'] is False:
            logger.error(f"#### Get Accounts error : {res['data']}")
            return
        
        for data in res['data']:
            balance = Balance(**data)
            balance.created_at = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
            balance.order_uuid = order_uuid
            balance.acc_id = acc_id
            self._db_handler.insert_item(balance)


    def __calc_funds(self, trades):
        prices = 0.0
        avg = 0.0
        if trades is not None:
            for dic in trades:
                prices += float(dic['funds'])
            avg = prices / len(trades)
        return str(avg)
    
    def __calc_btc_price(self, trades):
        prices = 0.0
        if trades is not None:
            for dic in trades:
                prices += float(dic['price'])
        
        return str(prices)

    def __send_message(self, action, executed_price, btc_price, volume):
        
        message = []
        message.append(datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'))
        if action == "bid":
            message.append("[매수] 실행")
        elif action == "ask":
            message.append("[매도] 실행")
        message.append(f'거래 금액(BTC) : {btc_price}')
        message.append(f"거래 금액(가격) : {executed_price}")
        message.append(f"거래량 : {volume}")
        
        send_message = '\n'.join(message)
        
        TelegramBot().send_message(send_message)