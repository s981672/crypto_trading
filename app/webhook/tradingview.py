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
        logger.error(f'[TV_HOOK] EVENT PARSING ERROR : {payload}')
        return

    logger.info(f'[TV_HOOK] Receive WebHook : {now}')
    logger.info(f'[TV_HOOK] EVENT : {payload}')
    message =''
    for k,v in payload.items():
        message = message + f'{k} : {v}\n'
    TelegramBot().send_message(f'트레이딩뷰 이벤트 수신 : {now}\n\n{message}')


    tvEvent = TradingViewEvent(**payload)
    TradingViewController(event=tvEvent).newRun()
    return message
