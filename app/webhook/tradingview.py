from fastapi import APIRouter, Request
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
    TelegramBot.send_message(f'TradingView Event : {now}\n\n{message}')

    return message
