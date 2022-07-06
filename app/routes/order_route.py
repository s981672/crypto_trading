from urllib import response
from fastapi import APIRouter
from model.order_model import ApiResponse

from services.order_service import OrderService

router = APIRouter()

@router.post("/order")
async def order():
    """
    매수 또는 매도 주문을 진행한다.
    """
    response = OrderService.order(None)
    print(response)
    return response

@router.get("/order", response_model=ApiResponse)
async def get_order(uuid: str = None , identifier: str = None):
    
    """
    주문 정보를 조회한다.
    """
    return {
        'uuid' : uuid,
        'identifier' : identifier
    }

@router.delete("order")
async def delete_order():
    """
    주문 취소를 접수한다.
    """
    pass

@router.get("/orders/chance")
async def orders_chance(market: str):
    """
    주문 가능 정보를 조회한다.
    """
    response = OrderService.order_chance(market=market)
    return response

@router.get("/orders")
async def get_orders():
    """
    주문 리스트를 조회한다.
    """
    pass