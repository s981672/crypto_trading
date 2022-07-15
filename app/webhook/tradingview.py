from fastapi import APIRouter, Request
from controller.tradingview_controller import TradingViewController
from models.trading_view_event import TradingViewEvent
from pusher.telegram import TelegramBot
import datetime

router = APIRouter()

@router.post("/tv/webhook")
async def tradingview_webhook(request: Request):
    
    """
    TradingView WebHook 수신
    """
    now = datetime.datetime.now()
    payload = await request.json()

    message =''
    for k,v in payload.items():
        message = message + f'{k} : {v}\n'
    TelegramBot.send_message(f'트레이딩뷰 이벤트 수신 : {now}\n\n{message}')


    tvEvent = TradingViewEvent(**payload)
    TradingViewController(event=tvEvent).run()
    return message
