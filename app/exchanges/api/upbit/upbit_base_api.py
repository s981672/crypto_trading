
import hashlib
from typing import Dict, Union
from urllib.parse import unquote, urlencode
import uuid

import jwt
import requests
from exchanges.api.base_api import BaseApi


class UpbitBaseApi(BaseApi):
    
    def __get_header(self, **kwargs):
        query_hash: str = self.__encode_kwargs(**kwargs)
        
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
    
    def __encode_kwargs(self, **kwargs) -> Union[str, None]:
        if kwargs is None:
            return None
        
        querys = []
        query_hash: str = None        
        for k,v in kwargs.items():
            if v is None:
                pass
            elif type(v) is list:
                joined_kv = '&'.join([(k+"[]={}").format(value) for value in v])
                querys.append(joined_kv)
            else:
                querys.append(f'{k}={v}')

        if len(querys) > 0:
            query_string = '&'.join(querys).encode()
            print(query_string)
            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()
       
        return query_hash

    def __get_params(self, **kwargs):
        params = {}
        for k,v in kwargs.items():
            if v is None:
                pass
            elif type(v) is list:
                params[f'{k}[]'] = v
            else:
                params[k] = v
        return params
    
    def __request(
        self,
        api,
        url: str,
        **kwargs
    ):
        headers = self.__get_header(**kwargs)
        params = self.__get_params(**kwargs)
        
        res = api(url, params=params, headers=headers)
        
        print(f'HTTP STATUS_CODE : {res.status_code}')
        
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
        