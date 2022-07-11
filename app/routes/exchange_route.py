from email.policy import default
from typing import List, Optional, Union
from fastapi import APIRouter, Query
from isort import stream
from services.exchange_service import ExchangeService

router = APIRouter()

@router.get("/accounts")
async def get_accounts(
    exchange: str = "upbit",
    access: str = "DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P",
    secret: str = "fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt"
):
    """
    계좌 정보를 조회한다.
    """
    response = ExchangeService.accounts(exchange, access, secret)
    return response
    
@router.get("/order/chance")
async def get_order_chance(
    exchange: str = "upbit",
    access: str = "DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P",
    secret: str = "fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt",
    market: str = "KRW-BTC"
):
    response = ExchangeService.order_chance(exchange, access, secret, market)
    return response

@router.post("/order")
async def order(
    exchange: str,
    access: str,
    secret: str,
    market: str,
    side: str,
    ord_type: str,
    volume: str = None,
    price: str = None,
    identifier: Optional[str] = None,
    ):
    """
    매수 또는 매도 주문을 진행한다.
    """
    response = ExchangeService.post_order(exchange, access, secret, market, side, volume, price, ord_type, identifier)
    return response

@router.get("/order")
async def get_order_info(
    exchange: str,
    access: str,
    secret: str,
    uuid: str = None , 
    identifier: str = None):
    
    """
    주문 정보를 조회한다.
    """
    response = ExchangeService.get_order_info(exchange, access, secret, uuid, identifier)
    return response

@router.delete("order")
async def delete_order(
    exchange: str,
    access: str,
    secret: str,
    uuid: str = None , 
    identifier: str = None):
    """
    주문 취소를 접수한다.
    """
    response = ExchangeService.delete_order(exchange, access, secret, uuid, identifier)
    return response

@router.get("/orders")
async def get_orders_info(
    state: str,
    page: int = 1,
    limit: int = 100,
    states: Union[List[str], None] = Query(default=None),
    identifiers: Union[List[str], None] = Query(default=None),
    uuids: Union[List[str], None] = Query(default=None),
    order_by: str = "desc",
    exchange: str = "upbit",
    access: str = "DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P",
    secret: str = "fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt",
    market: str = "KRW-BTC"
):
    """
    주문 리스트를 조회한다.
    """
    response = ExchangeService.get_orders_info(
        exchange,
        access,
        secret,
        market,
        uuids,
        identifiers,
        state,
        states,
        page,
        limit,
        order_by
        )
    
    return response