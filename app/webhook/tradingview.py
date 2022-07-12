from fastapi import APIRouter, Request
from pusher.telegram import TelegramBot

router = APIRouter()

@router.post("/tv/webhook")
async def tradingview_webhook(request: Request):
    """
    TradingView WebHook 수신
    """
    print(request)
    data = await request.json()
    # print(data)
    TelegramBot.send_message(f'트레이딩뷰 웹훅 수신.\n')
    return 'Received WebHook'

