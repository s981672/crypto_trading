

from typing import List
from exchanges.api.upbit.quotation_api import QuotationApi
from exchanges.api.upbit.exchange_api import ExchangeApi
from exchanges.error.errors import InvalidMarketNameError

###############
# EXCHANGE API
###############

def __get_exchange_api(
    exchange: str,
    access: str,
    secret: str
    ):
    if exchange == "upbit":
        return ExchangeApi(access,secret)
    
    raise InvalidMarketNameError()

def get_accounts(
    exchange: str, 
    access: str,
    secret: str,
    ):
    """
    계좌 정보 조회
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.get_accounts()
    except Exception as e:
        # log 처리 후 raise
        pass
    

def get_orders_chance(
    exchange: str,
    access: str,
    secret: str,
    market: str,
    ):
    """
    마켓별 주문 가능 정보를 확인
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.get_orders_chance(market)
    except Exception as e:
        # log 처리 후 raise
        pass


def get_order_info(
    exchange: str,
    access: str,
    secret: str,
    uuid: str,
    identifier: str = None,    
):
    """
    개별 주문 조회
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.get_order_info(uuid, identifier)
    except Exception as e:
        # log 처리 후 raise
        pass

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
    """
    주문 목록 조회
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.get_orders_info(market, uuids, identifiers, state, states, page, limit, order_by)
    except Exception as e:
        # log 처리 후 raise
        pass

def delete_order(
    exchange: str,
    access: str,
    secret: str,
    uuid: str,
    identifier: str,    
):
    """
    주문 취소 요청
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.delete_order(uuid, identifier)
    except Exception as e:
        # log 처리 후 raise
        pass
    
def post_order(
    *,
    exchange: str,
    access: str,
    secret: str,
    market: str,
    side: str,
    ord_type: str,
    volume: str = None,
    price: str = None,
    identifier: str = None
):
    """
    주문 요청
    """
    try:
        api = __get_exchange_api(exchange, access, secret)
        return api.post_order(market, side, volume, price, ord_type, identifier)
    except Exception as e:
        # log 처리 후 raise
        pass

###############
# QUOTATION API
###############
def __get_quotation_api(
    exchange: str,
):
    if exchange == "upbit":
        return QuotationApi()
    
    raise InvalidMarketNameError()

def get_order_book(
    exchange: str,
    markets: List[str]
):
    try:
        api = __get_quotation_api(exchange)
        return api.get_order_book(markets)
    except Exception as e:
        pass