
import logging
from algorithm.base_algorighm import BaseAlgorithm
from models.mariadb.algorithm import Algorithm
from models.mariadb.algorithm_list import AlgorithmList
from database.mariadb_handler import MariadbHandler
from models.trading_view_event import TradingViewEvent


class B7125(BaseAlgorithm):
    logger = logging.getLogger('sLogger')
    
    def run_algorithm(self):
        """
            1. 해당 이벤트에 해당하는 전략을 찾는다.
            2. 현재 Postion을 갖고 있는지 체크한다.
            3. Event가 Buy인 경우 매수를 요청한다. 만약 Position이 있는 경우에는 무시한다.
            4. Event가 Sell인 경우 매도를 요청한다. 만약 Position이 없는 경우에는 무시한다.
        """
        self._alg_list = self._db_handler.find_items(AlgorithmList, {
            "algorithm_id":self._event.strategy_id,
            "sub_algorithm_id":self._event.order_id
            })
        self._alg = self._db_handler.find_items(Algorithm, {
            "algorithm_id":self._event.strategy_id
            })
        if self._alg is None or len(self._alg) == 0:
            self.logger.warning(f'# No Algorighm. strategy_id : {self._event.strategy_id}, order_id : {self._event.order_id}')
            return

        if self._alg_list is None or len(self._alg_list) == 0:
            self.logger.warning(f'# No Algorighm. strategy_id : {self._event.strategy_id}, order_id : {self._event.order_id}')
            return

        self.logger.debug(f'Find Strategy')
        
        if self._event.action == 'buy':
            self.__buy()            
        else:
            self.__sell()

    def __buy(self):
        self.logger.debug(f'Buy. exchange:{self._alg[0].exchange}, market:{self._alg[0].market}')
        self.buy(
            exchange=self._alg[0].exchange,
            market=self._alg[0].market,
            ord_type='price',
            algorithm_list=self._alg_list[0]
        )
        
    def __sell(self):
        volume = self._alg_list[0].executed_volume
        if volume is None or volume == "0.0":
            self.logger.warning(f'There is no Volume. exchange:{self._alg[0].exchange}, market:{self._alg[0].market}')
            return
        
        self.logger.debug(f'Sell. exchange:{self._alg[0].exchange}, market:{self._alg[0].market}, volume:{volume}')
        self.sell(
            exchange=self._alg[0].exchange,
            market=self._alg[0].market,
            ord_type='market',
            algorithm_list=self._alg_list[0]
        )
