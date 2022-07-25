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

class TelegramBot():
    last_update_id: int = -1
    
    def __init__(self):
        self._bot = tel.Bot(token='5442796506:AAHjEtCo1-lE9hqWSTnRUnIcAWR8JdnOQB0')
        self._chat_ids = ['383832259', '1819858493']
    
    def send_message(self, message:str = ""):
        for chat_id in self._chat_ids:
            self._bot.sendMessage(chat_id, message)

    def get_update(self):
        update = self._bot.get_updates()
        message_id = update[-1]['message']['message_id']
        if message_id is not self.last_update_id:
            self.last_update_id = message_id
            print(f'Message Update : {self.last_update_id}')
        