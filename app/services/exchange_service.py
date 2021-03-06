

from copy import copy, deepcopy
import json
from typing import List
from common.const import DBConst
from controller.tradingview_controller import TradingViewController
from models.trading_view_event import TradingViewEvent
from models.strategy import Strategy
from dao import strategy_dao, order_book_dao
from database.mongodb_handler import MongoDBHandler
from pusher.telegram import TelegramBot
import exchanges.main as ex


class ExchangeService():

    @staticmethod
    def accounts(
        exchange: str,
        access: str,
        secret: str
    ):
        res = ex.get_accounts(exchange, access, secret)
        
        return res

    @staticmethod
    def order_chance(
        exchange: str,
        access: str,
        secret: str,
        market: str
    ):
        res = ex.get_orders_chance(exchange, access, secret, market)

        return res

    @staticmethod
    def get_order_info(
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        res = ex.get_order_info(exchange, access, secret, uuid, identifier)

        event = {
            "strategy_id" : "B000000",
            "ticker" : "BTCKRW",
            "order_id" : "L1",
            "action" : "sell",
            "contracts" : "0.003464",
            "price" : "27120000",
            "position_size" : "0.006928"
        }

        tvEvent = TradingViewEvent(**event)
        TradingViewController(event=tvEvent).newRun()

        return res

    @staticmethod
    def get_orders_info(
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
        res = ex.get_orders_info(exchange, access, secret, market, uuids, identifiers, state, states, page, limit, order_by)

        return res

    @staticmethod
    def delete_order(
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        res = ex.delete_order(exchange, access, secret, uuid, identifier)

        return res

    @staticmethod
    def post_order(
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
                
        return res

    @staticmethod
    def get_order_book(
        exchange: str,
        markets: List[str]
    ):
        res = ex.get_order_book(exchange, markets)

        # if res.status_code == 200:
        #     json_data = json.loads(res.text)
        #     order_book_dao.create_order_book(json_data)
        
        return res
    
