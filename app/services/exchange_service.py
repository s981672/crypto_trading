

from typing import List
from pusher.telegram import TelegramBot
import exchanges.main as ex
from utils.logger import Log


class ExchangeService():

    @staticmethod
    def accounts(
        exchange: str,
        access: str,
        secret: str
    ):
        res = ex.get_accounts(exchange, access, secret)
        TelegramBot.send_message(res)

        return res

    @staticmethod
    def order_chance(
        exchange: str,
        access: str,
        secret: str,
        market: str
    ):
        return ex.get_orders_chance(exchange, access, secret, market)

    @staticmethod
    def get_order_info(
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        return ex.get_order_info(exchange, access, secret, uuid, identifier)

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
        return ex.get_orders_info(exchange, access, secret, market, uuids, identifiers, state, states, page, limit, order_by)

    @staticmethod
    def delete_order(
        exchange: str,
        access: str,
        secret: str,
        uuid: str,
        identifier: str
    ):
        return ex.delete_order(exchange, access, secret, uuid, identifier)

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
        return ex.post_order(
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
