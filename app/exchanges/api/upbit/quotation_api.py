

import json
import requests
from exchanges.common.url import UpbitUrl
from exchanges.api.base_api import BaseQuotationApi


class QuotationApi(BaseQuotationApi):
    
    def __get_params(self, **kwargs):
        querys = []
        for k,v in kwargs.items():
            if v is None:
                pass
            elif type(v) is list:
                joined_kv = '&'.join([(k+"={}").format(value) for value in v])
                querys.append(joined_kv)
            else:
                querys.append(f'{k}={v}')

        if len(querys) > 0:
            queyr_param = '&'.join(querys)
            return queyr_param
    
        return None
    
    def get_order_book(
        self,
        markets
    ):

        query_param = self.__get_params(markets=markets)
        res = requests.get(UpbitUrl.URL_ORDER_BOOK, query_param)
        return res