

class UpbitUrl:
    PROD_URL = "https://api.upbit.com"
    VERSION_PREFIX = "/v1"
    
    URL_ACCOUNTS = PROD_URL + VERSION_PREFIX + "/accounts"
    URL_ORDER = PROD_URL + VERSION_PREFIX + "/order"
    URL_ORDERS = PROD_URL + VERSION_PREFIX + "/orders"
    URL_ORDER_CHANCE = PROD_URL + VERSION_PREFIX + "/orders/chance"
    
    URL_ORDER_BOOK = PROD_URL + VERSION_PREFIX + "/orderbook"
    
class BinanceUrl:
    pass