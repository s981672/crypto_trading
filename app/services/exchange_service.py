

from copy import copy, deepcopy
from typing import List
from models.strategy import Strategy
from dao import strategy_dao
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
            volume,
            price,
            ord_type,
            identifier
        )
        
        TelegramBot().send_message(f'주문을 요청합니다.\n주문 결과:{res}')
        mongodb = MongoDBHandler("141.164.48.85")
        mongodb.insert_item(deepcopy(res['data']), "bml_trader", "orders")
        
        return res
