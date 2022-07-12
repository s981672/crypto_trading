# from telethon import TelegramClient

# class TelegramBot():

#     def __init__(self):
#         """텔레그램으로 메시지를 보내기 위한 PushTelegram 클래스입니다.
#         config.ini파일로 부터 api_id와 api_hash를 읽어옵니다. 
#         TelegramClient 생성시 app name과 api_id, api_hash를 파라미터로 전달합니다.
#         """
#         # api_id = 14933104
#         # api_hash = '6a57489cd166ea102d3215e995edee8c'
#         # self.telegram = TelegramClient("session", api_id, api_hash)
#         # assert self.telegram
        
#     async def send_message(self, username=None, message=None):
#         """
#         Args:
#             username(str): 보낼 유저명
#             message(str): 보낼 메시지
#         """
#         api_id = 14933104
#         api_hash = '6a57489cd166ea102d3215e995edee8c'
#         self.telegram = TelegramClient("session", api_id, api_hash)
        
#         self.telegram.start()
        
#         entity = await self.telegram.get_entity("821029447832")
#         self.telegram.send_message(entity=entity, message=message)

import telegram as tel

class TelegramBot:
    
    @staticmethod
    def send_message(message:str = ""):
        bot = tel.Bot(token='5442796506:AAHjEtCo1-lE9hqWSTnRUnIcAWR8JdnOQB0')
        chat_id = '383832259'

        bot.sendMessage(chat_id=chat_id , text=message)