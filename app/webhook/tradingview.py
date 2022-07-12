from fastapi import APIRouter
from pusher.telegram import TelegramBot

router = APIRouter()

@router.post("/tv/webhook")
async def tradingview_webhook():
    """
    TradingView WebHook 수신
    """
    TelegramBot.send_message(f'트레이딩뷰 웹훅 수신.\n')
    return 'Received WebHook'
