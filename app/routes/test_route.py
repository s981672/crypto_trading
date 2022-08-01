from typing import List, Optional, Union
from fastapi import APIRouter, Query
from isort import stream
from services.exchange_service import ExchangeService

from controller.tradingview_controller import TradingViewController
from models.trading_view_event import TradingViewEvent
from pytz import timezone
from pusher.telegram import TelegramBot
from datetime import datetime

router = APIRouter()

@router.post("/test/webhook")
async def webhook_event(
    strategy_id: str = "B000000",
    ticker: str = "KRW-BTC",
    order_id: str = "L[1]",
    action: str = "buy",
    contracts: str = "0.00001",
    price: str = "1000000",
    position_size: str = "100",
    ):
    """
    매수 또는 매도 주문을 진행한다.
    """

    event = {'strategy_id': strategy_id, 
             'ticker': ticker, 
             'order_id': order_id, 
             'action': action, 
             'contracts': contracts, 
             'price': price, 
             'position_size': position_size}

    now = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    message = __get_message(event)
    TelegramBot().send_message(f'[Signal]\n{now}\n{message}')


    tvEvent = TradingViewEvent(**event)
    TradingViewController(event=tvEvent).newRun()
    return 


def __get_message(payload):
    message =''
    ignoreKeys = ['contracts', 'position_size']
    for k,v in payload.items():
        # starategy_id 는 alog id로 이름을 변경한다.
        if k == 'strategy_id' :
            k = 'alog id'
        # 필요없는 메시지는 보내지 않도록 한다.
        if k in ignoreKeys:
            continue     
        message = message + f'{k} : {v}\n'
        
    return message
