

from typing import List
import uuid

import jwt
from exchanges.common.url import UpbitUrl

from exchanges.api.upbit.upbit_base_api import UpbitBaseApi


class ExchangeApi(UpbitBaseApi):

    def get_accounts(self):
        """
        자산 정보를 조회
        """

        res = self.request_get(UpbitUrl.URL_ACCOUNTS)
        
        return res

    
    def get_orders_chance(
        self,
        market: str
    ):
        """
        마켓별 주문 가능 정보 확인

        Args:
            market (str): 마켓 정보
        """
        res = self.request_get(UpbitUrl.URL_ORDER_CHANCE, market=market)
        
        return res
    
    def get_order_info(
        self,
        uuid: str,
        identifier: str,
    ):
        """
        주문 정보  조회.
        UUID 또는 Identifier 중에 하나의 값이 포함되어야 함.

        Args:
            uuid (str): 주문 UUID 정보
            identifier (str): 주문 Custom ID 정보
        """
        res = self.request_get(
            UpbitUrl.URL_ORDER, 
            uuid=uuid,
            identifier=identifier)
        
        return res
    
    def get_orders_info(
        self,
        market: str,
        uuids: List[str],
        identifiers: List[str],
        state: str,
        states: List[str],
        page: int = 1,
        limit: int = 100,
        order_by: str = "desc"
    ):
        """
        주문 리스트를 조회

        Args:
            market (str): _description_
            uuids (List[str]): _description_
            identifiers (List[str]): _description_
            state (str): _description_
            states (List[str]): _description_
            page (int, optional): _description_. Defaults to 1.
            limit (int, optional): _description_. Defaults to 100.
            order_by (str, optional): _description_. Defaults to "desc".
        """
        res = self.request_get(
            UpbitUrl.URL_ORDERS, 
            market=market,
            uuids=uuids,
            identifiers=identifiers,
            state=state,
            states=states,
            page=page,
            limit=limit,
            order_by=order_by
            )

        return res
    
    def delete_order(
        self,
        uuid: str,
        identifier: str
    ):
        """
        주문을 취소 요청

        Args:
            uuid (str): _description_
            identifier (_type_): _description_
            str (_type_): _description_
        """
        res = self.request_delete(
            UpbitUrl.URL_ORDER, 
            uuid=uuid,
            identifier=identifier)
        
        return res
    
        
    def post_order(
        self,
        market: str,
        side: str,
        volume: str,
        price: str,
        ord_type: str,
        identifier: str
    ):
        """
        주문 요청
        """
        res = self.request_post(
            UpbitUrl.URL_ORDERS,
            market=market,
            side=side,
            volume=volume,
            price=price,
            ord_type=ord_type,
            identifier=identifier
        )

        return res