

from abc import ABCMeta, abstractclassmethod, abstractmethod
import json
from datetime import datetime
from logging import Logger, log, warning
import logging
import os
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

logger = logging.getLogger('sLogger')

class BaseAlgorithm(metaclass=ABCMeta):
    
    def __init__(self, event:TradingViewEvent = None):
        self._db_handler = MariadbHandler()
        self.__get_keys()
        self._event = event

    def __get_keys(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        with open(f'{basedir}/../keys.json') as f:
            config = json.load(f)

        self._access = config['upbit']['access']
        self._secret = config['upbit']['secret']

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
        logger.info(f"Enable Order Price: {enable_money}")
        return str(enable_money)
    
    def __calc_sell_volume(self, algorithm_list:AlgorithmList):
        current_volume = double(algorithm_list.executed_volume)
        logger.info(f"Enable Sell Order Volume : {current_volume}")
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

        logger.info(f'Buy : exchange:{exchange}, market:{market}, price:{price}')
        
        # 1. 지정된 금액을 기준으로 매수 요청.
        try:
            res = ex.post_order(
                exchange=exchange, 
                access=self._access, 
                secret=self._secret, 
                market=market, 
                side='bid', 
                ord_type=ord_type,
                price=price)
        except Exception as e:
            logger.error(f'[BUY]POST ORDER ERROR : {e}')
            return               
        
        if res is None or res['success'] == False :
            logger.error(f'[BUY]POST ORDER FAILED : {res}')
            return
        
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
        
        logger.info(f'Sell : exchange:{exchange}, market:{market}, volume:{volume}')

        try:
            res = ex.post_order(
                exchange=exchange, 
                access=self._access, 
                secret=self._secret, 
                market=market, 
                side='ask', 
                ord_type=ord_type,
                volume=volume)
        except Exception as e:
            logger.error(f'[SELL]POST ORDER ERROR : {e}')
            return               
        
        if res is None or res['success'] == False :
            logger.error(f'[SELL]POST ORDER FAILED : {res}')
            return
        
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
            
            if res['success'] is True and (res['data']['state'] == "cancel" or res['data']['state'] == "done"):
                check_completed = True
                # Trade 정보를 DB에 쌓는다
                tradeData = res['data']['trades']
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
                self.__send_message(algorithm_list, orderData)

            else:
                time.sleep(1)



    def __update_algorithm_list(self, orderData:Dict, algorithm_list:AlgorithmList):
        (total_money, total_volume) = self.__calc_total_volume_and_price(orderData, algorithm_list)
        algorithm_list.total_money = str(total_money)
        algorithm_list.executed_volume = str(total_volume)
        algorithm_list.updated_at = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        
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

    # def __send_message(self, action, executed_price, btc_price, volume):
        
    #     message = []
    #     message.append(datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'))
    #     if action == "bid":
    #         message.append("[매수] 실행")
    #     elif action == "ask":
    #         message.append("[매도] 실행")
    #     message.append(f'거래 금액(BTC) : {btc_price}')
    #     message.append(f"거래 금액(가격) : {executed_price}")
    #     message.append(f"거래량 : {volume}")
        
    #     send_message = '\n'.join(message)
        
    #     TelegramBot().send_message(send_message)
        
    def __send_message(self, algorithm_list:AlgorithmList, orderData):
        """
        [Trade]
        2022-02-02 08:02:14                 => 날짜
        account_id : U123456                => acc_id , algorithm_list에 존재
        algo id : B712503                   => algorithm_id, algorithm_list에 존재
        ticker : ETHKRW                     => order response의 market 값
        order_id : L[2]                     => sub_algorithm_id, algorithm_list에 존재
        action : buy                        => order response의 side 값으로 판단.
        매수시 총체결목표금액 : 10000 KRW     => order response 의 price
        매수시 실체결금액 : 9900 KRW          => trades의 funds 합계
        (매도시 총체결목표계약수 : 0.00031      => order response의 volume
        매도시 실체결계약수 :  0.00030)         => order response의 executed_volume
        1차체결 price:                          => trade의 price
        1차체결 contracts (계약수) : 0.00032    => trade의 voluem
        1차체결 trade amout (거래금액) : 5500   => trade의 funds
        """
        message = []
        message.append("[Trade]")
        message.append(datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'))
        message.append(f"account_id : {algorithm_list.acc_id}")
        message.append(f"alog_id : {algorithm_list.algorithm_id}")
        message.append(f"ticker : {orderData['market']}")
        message.append(f"order_id : {algorithm_list.sub_algorithm_id}")
        
        total_price = 0.0
        total_volume = 0.0
        total_funds = 0.0
        trade_message = []
        for idx, trade in enumerate(orderData['trades'], 1):
            trade_message.append(f"{idx}차 가격: {trade['price']}")
            if orderData['side'] == 'bid':
                trade_message.append(f"{idx}차 금액: {trade['funds']}")
            else:
                trade_message.append(f"{idx}차 계약수: {trade['volume']}")
            total_price += float(trade['price'])
            total_volume += float(trade['volume'])
            total_funds += float(trade['funds'])
            
        if orderData['side'] == 'bid':
            message.append(f"action : buy")    
            rate = round(total_funds / float(orderData['price']) * 100 ,2)
            message.append(f"체결율(체결금액/주문금액) : {rate}% ({total_funds}/{orderData['price']})")
            # message.append(f"매수시 총체결목표금액: {orderData['price']}")
            # message.append(f"매수시 실체결금액: {str(total_funds)}")
        else:
            message.append(f"action : sell")    
            rate = round(total_volume / float(orderData['volume']) * 100 ,2)
            message.append(f"체결율(체결계약수/주문계약수) : {rate}% ({total_volume}/{orderData['volume']})")
            # message.append(f"매도시 총체결목표계약수: {orderData['volume']}")
            # message.append(f"매도시 실체결계약수: {str(total_volume)}")
        
        message.extend(trade_message)
        
        
        send_message = '\n'.join(message)
        
        TelegramBot().send_message(send_message)        