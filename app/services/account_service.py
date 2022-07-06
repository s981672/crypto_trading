

import apis.upbit.account_api as upbitApi
import apis.binance.account_api as binanceApi
from utils.logger import Log


class AccountService():
    
    @staticmethod
    def accounts():
        api = upbitApi.AccountApi()
        return api.account()