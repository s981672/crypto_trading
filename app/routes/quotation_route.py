from typing import List, Optional, Union
from fastapi import APIRouter, Query
from isort import stream
from services.exchange_service import ExchangeService

router = APIRouter()

@router.get("/order_book")
async def get_order_book(
    exchange: str,
    markets: Union[List[str], None] = Query(default=None)
):
    """
    계좌 정보를 조회한다.
    """
    response = ExchangeService.get_order_book(exchange, markets)
    return response.text
    
