
import hashlib
from typing import Dict
from urllib.parse import unquote, urlencode
import uuid

import jwt
import requests
from exchanges.api.base_api import BaseApi


class UpbitBaseApi(BaseApi):
    
    def __get_header(self, **kwargs):
        query_hash: str = None
        
        if kwargs:
            setted_kwargs = {k:v for k,v in kwargs.items() if v is not None}
            query_string = urlencode(setted_kwargs).encode()
            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()
            
        payload = {
            'access_key': self.access,
            'nonce': str(uuid.uuid4()),
        }

        if query_hash is not None:
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = 'SHA512'

        jwt_token = jwt.encode(payload, self.secret)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {
            "Authorization": authorize_token,
            "Accept": "application/json"
            }
        
        return headers
    
    def __request(
        self,
        api,
        url: str,
        **kwargs
    ):
        headers = self.__get_header(**kwargs)
        res = api(url, params=kwargs, headers=headers)
        
        return {
            'success' : res.status_code == 200,
            'data': res.json()
        }
        
    
    def request_post(self, url: str, **kwargs):
        return self.__request(requests.post, url, **kwargs)
    
    def request_get(self, url: str, **kwargs):
        return self.__request(requests.get, url, **kwargs)
    
    
    def request_delete(self, url: str, **kwargs):
        return self.__request(requests.delete, url, **kwargs)
        