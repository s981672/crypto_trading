import logging
from fastapi import APIRouter, Request
from pytz import timezone
from controller.tradingview_controller import TradingViewController
from models.trading_view_event import TradingViewEvent
from pusher.telegram import TelegramBot
from datetime import datetime

router = APIRouter()

logger = logging.getLogger('sLogger')

@router.post("/tv/webhook")
async def tradingview_webhook(request: Request):
    
    """
    TradingView WebHook 수신
    """
    now = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f'[TV_HOOK] EVENT PARSING ERROR')
        return

    logger.info(f'[TV_HOOK] Receive WebHook : {now}')
    logger.info(f'[TV_HOOK] EVENT : {payload}')

    message = __get_message(payload)
    TelegramBot().send_message(f'[Signal]\n{now}\n{message}')

    tvEvent = TradingViewEvent(**payload)
    TradingViewController(event=tvEvent).newRun()

    return message


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
