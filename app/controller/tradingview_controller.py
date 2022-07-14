
from pymongo import MongoClient
from app.database.mongodb_handler import MongoDBHandler
from app.models.trading_view_event import TradingViewEvent
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
        self._db_handler=MongoDBHandler(db_name="bml_trader")
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
        pass
        
        
    def __sell(self):
        _volume = '123'
        
        res = ex.post_order('upbit', self._access, self._secret, 'KRW-BTC', 'ask', _volume)
        # DB Insert
        
        pass
    
    def __order(self):
        pass

    def __contract_thread(self, order):
        # UUID를 기반으로 거래 정보를 조회하여 체결 여부 확인
        # 체결 여부는 state가 done, cancel로 바뀌어야 함.
        # trade_count가 0 이면 취소가 된 것으로 간주.
        # 체결 여부 확인 후 결과를 Telegram으로 전송
        pass
        