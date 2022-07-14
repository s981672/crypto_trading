
import unittest

from app.pusher.telegram import TelegramBot


class TelegramTest(unittest.TestCase):
    def setUp(self) -> None:
        pass
    
    def tearDown(self) -> None:
        pass
    
    def send_message(self):
        TelegramBot.send_message("Unit Test")
        
    