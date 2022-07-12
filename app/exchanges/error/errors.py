

from typing import Any


class BaseExchangeError(Exception):
    name: str
    code: int
    message: str
    
    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ctx

    def __str__(self) -> str:
        return self.msg.format(**self.__dict__)


class InvalidMarketNameError(BaseExchangeError):
    name = "Invalid Market Name Error"
    code = 600
    message = "마켓 이름이 잘못 되었습니다."
    
class ExchangeAPIError(BaseExchangeError):
    name = "Exchange API Error"
