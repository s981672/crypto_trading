

import logging
from typing import List
import exchanges.main as ex


class ExchangeService():
    _logger = logging.getLogger('sLogger')
    
    @classmethod
    def accounts(
        cls,
        exchange: str,
        access: str,
        secret: str
    ):
        try:
            res = ex.get_accounts(exchange, access, secret)
        except Exception as e:
            cls._logger.error(f'Account Error : {e}')
            return {'success' : False, 'data' : e}
        
        return res

    @classmethod
    def order_chance(
        cls,
        exchange: str,
        access: str,
        secret: str,
        market: str
    ):
        try:
            res = ex.get_orders_chance(exchange, access, secret, market)
        except Exception as e:
            cls._logger.error(f'Order Chance Error : {e}')
            return {'success' : False, 'data' : e}

        return res

    @classmethod
    def get_order_info(
        cls,
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        try:
            res = ex.get_order_info(exchange, access, secret, uuid, identifier)
        except Exception as e:
            cls._logger.error(f'Order Info Error : {e}')
            return {'success' : False, 'data' : e}

        # event = {
        #     "strategy_id" : "B000000",
        #     "ticker" : "BTCKRW",
        #     "order_id" : "L1",
        #     "action" : "sell",
        #     "contracts" : "0.003464",
        #     "price" : "27120000",
        #     "position_size" : "0.006928"
        # }

        # tvEvent = TradingViewEvent(**event)
        # TradingViewController(event=tvEvent).newRun()

        return res

    @classmethod
    def get_orders_info(
        cls,
        exchange: str,
        access: str,
        secret: str,
        market: str,
        uuids: List[str],
        identifiers: List[str],
        state: str,
        states: List[str],
        page: int,
        limit: int,
        order_by: str,
    ):
        try:
            res = ex.get_orders_info(exchange, access, secret, market, uuids, identifiers, state, states, page, limit, order_by)
        except Exception as e:
            cls._logger.error(f'Order Info Error : {e}')
            return {'success' : False, 'data' : e}

        return res

    @classmethod
    def delete_order(
        cls,
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        try:
            res = ex.delete_order(exchange, access, secret, uuid, identifier)
        except Exception as e:
            cls._logger.error(f'Delete Order Error : {e}')
            return {'success' : False, 'data' : e}

        return res

    @classmethod
    def post_order(
        cls,
        exchange: str,
        access: str,
        secret: str,
        market: str,
        side: str,
        volume: str,
        price: str,
        ord_type: str,
        identifier: str = None
    ):
        try:
            res = ex.post_order(
                exchange,
                access,
                secret,
                market,
                side,
                ord_type,
                volume,
                price,
                identifier
            )
        except Exception as e:
            cls._logger.error(f'post Order Error : {e}')
            return {'success' : False, 'data' : e}
                
        return res

    @classmethod
    def get_order_book(
        cls,
        exchange: str,
        markets: List[str]
    ):
        try:
            res = ex.get_order_book(exchange, markets)
        except Exception as e:
            cls._logger.error(f'Order Book Error : {e}')
            return {'success' : False, 'data' : e}

        # if res.status_code == 200:
        #     json_data = json.loads(res.text)
        #     order_book_dao.create_order_book(json_data)
        
        return res
    
