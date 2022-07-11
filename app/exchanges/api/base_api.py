

from abc import ABCMeta, abstractmethod
from typing import List


class BaseApi(metaclass=ABCMeta):
    access: str
    secret: str
    
    def __init__(
        self,
        access: str = None,
        secret: str = None
    ):
        self.access = access
        self.secret = secret
    

class ExchangeApi(BaseApi):
    @abstractmethod
    def get_accounts(self):
        """
        자산 정보를 조회
        """
        pass
    
    @abstractmethod
    def get_orders_chance(
        self,
        market: str
    ):
        """
        마켓별 주문 가능 정보 확인

        Args:
            market (str): 마켓 정보
        """
        pass  
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_orders(
        self,
        # market: str,
        # uuids: List[str],
        # identifiers: List[str],
        # state: str,
        # states: List[str],
        # page: int = 1,
        # limit: int = 100,
        # order_by: str = "desc"
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
        pass
    
    @abstractmethod
    def delete_order(
        uuid: str,
        identifier, str
    ):
        """
        주문을 취소 요청

        Args:
            uuid (str): _description_
            identifier (_type_): _description_
            str (_type_): _description_
        """
        pass
    
    @abstractmethod
    def req_order(
        market: str,
        side: str,
        volume: float,
        price: float,
        ord_type: str,
        identifier: str
    ):
        """
        주문 요청

        Args:
            market (str): _description_
            side (str): _description_
            volume (float): _description_
            price (float): _description_
            ord_type (str): _description_
            identifier (str): _description_
        """
        pass