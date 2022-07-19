
from datetime import datetime
import json
import time
from dao import order_book_dao
from common.const import DBConst
from pusher.telegram import TelegramBot
from dao import strategy_dao
from models.order import Order
from models.strategy import Strategy
from dao import order_dao
from database.mongodb_handler import MongoDBHandler
from error.error import ExchangeApiError
from models.trading_view_event import TradingViewEvent
import exchanges.main as ex

def handle_trading_view_event(self, event):
    """
    트레이딩뷰로부터 온 이벤트를 받아서 파싱 처리
    """
    if event is None:
        # EVENT가 없으면 처리할 게 없음
        return
        
    trading_view_controller = TradingViewController(event)
    trading_view_controller.run()
    

class TradingViewController:
    
    def __init__(self, event:TradingViewEvent = None):
        self._db_handler=MongoDBHandler(db_name=DBConst.DB_NAME)
        self._access = 'DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P'
        self._secret = 'fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt'
        self._event = event
        
    def run(self):
        """
        전략에 따라 매수 매도를 진행한다.
        1. 계좌 정보를 조회.
        2. 이벤트에 따라 매수/매도를 진행
        3. 타이머를 돌면서 매수/매도 완료 여부를 체크
        """
        print(f'#### 텔레그램 이벤트 수신 : {self._event}')
        if self._event.action == "buy":
            print('#### 매수 이벤트 수신')
            self.__buy()
        elif self._event.action == "sell":
            print("#### 매도 이벤트 수신")
            self.__sell()
        pass
        
        
    def __sell(self):
        # 현재 전략의 locked_volume의 값을 얻어와 매도를 실행
        cursor = strategy_dao.get_strategy("sungyol", self._event.strategy_id)
        if cursor is None:
            print("### stragy is not exist")
            return

        strategy: Strategy = None
        for dic in cursor:
            strategy = Strategy(**dic)
        
        if strategy is None or strategy.locked_volume is None:
            print("### locked volume is not exist")
            return
        
        if strategy.locked_volume is not None and strategy.locked_volume == "0.0":
            print("### locked volume is 0.0")
            return
        
        print(f'#### 매도 진행 . volume: {strategy.locked_volume}')

        res = ex.post_order('upbit', self._access, self._secret, 'KRW-BTC', 'ask', ord_type="market", volume=strategy.locked_volume)
        
        if 'success' in res and res['success'] is True:
            print('#### 매도 성공. DB insert')
            order = order_dao.create_order("sungyol", self._event.strategy_id, res['data'], self._event.price)
            
            self.__get_order_book()

            self.__check_update_order(order, strategy)
        else:
            return

        
    
    def __buy(self):
        price = '6000'
        
        print('#### 매수 진행 ')
        res = ex.post_order('upbit', self._access, self._secret, 'KRW-BTC', 'bid', ord_type="price", price=price)

        print('### 매수 응답')
        print(res)
        
        if 'success' in res and res['success'] is True:
            print('#### 매수 성공. DB insert')
            order = order_dao.create_order("sungyol", self._event.strategy_id, res['data'], self._event.price)

            self.__get_order_book()

            self.__check_update_order(order)
        else:
            return
        

    def __contract_thread(self, order):
        # UUID를 기반으로 거래 정보를 조회하여 체결 여부 확인
        # 체결 여부는 state가 done, cancel로 바뀌어야 함.
        # trade_count가 0 이면 취소가 된 것으로 간주.
        # 체결 여부 확인 후 결과를 Telegram으로 전송
        pass
    
    def __get_order_book(self):
        res = ex.get_order_book("upbit", ['KRW-BTC'])
        if res.status_code == 200:
            jsonData = json.loads(res.text)
            order_book_dao.create_order_book(jsonData)
            
        
    def __check_update_order(self, order:Order, strategy:Strategy = None):
        
        check_completed = False
        
        while True:
            if check_completed is True:
                break
            
            res = ex.get_order_info("upbit", self._access, self._secret, order.uuid)
            print(res, res['success'], res['data']['state'])
            if res['success'] is True and (res['data']['state'] == "cancel" or res['data']['state'] == "done"):
                print('### 거래 결과 정보 수신')
                order_dao.update_order("sungyol", order.strategy_id, res['data'], "done")
                
                locked_volume = res['data']['executed_volume']
                if strategy is not None:
                    locked_volume = self.__calc_locked_volume(res['data']['executed_volume'], strategy.locked_volume)
                strategy_dao.update_strategy("sungyol", order.strategy_id, locked_volume=locked_volume)
                check_completed = True
                
                self.__send_message(order.order.side, 
                                    order.expected_price, 
                                    self.__calc_funds(res['data']['trades']),
                                    self.__calc_btc_price(res['data']['trades']),
                                    res['data']['executed_volume'])
            else:
                time.sleep(1)
                
    def __calc_locked_volume(self, executed_volume, locked_volume):
        executed_volume = float(executed_volume)
        locked_volume = float(locked_volume)
        clac_volume = locked_volume - executed_volume

        return str(clac_volume)
    
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
    
    def __send_message(self, action, expected_price, executed_price, btc_price, volume):
        
        message = []
        message.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if action == "bid":
            message.append("[매수] 실행")
        elif action == "ask":
            message.append("[매도] 실행")
        message.append(f"요청 금액 : {expected_price}")
        message.append(f'거래 금액(BTC) : {btc_price}')
        message.append(f"거래 금액(가격) : {executed_price}")
        message.append(f"거래량 : {volume}")
        
        send_message = '\n'.join(message)
        
        TelegramBot().send_message(send_message)