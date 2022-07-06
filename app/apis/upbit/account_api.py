
from apis.abstract_api import AbstractAccount

import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests


class AccountApi(AbstractAccount):
    
    def account(self):
        super().__init__()
        
        access_key = 'DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P'
        secret_key = 'fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt'
        server_url = 'https://api.upbit.com'

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {
            "Authorization": authorize_token,
            "Accept": "application/json"
            }

        res = requests.get(server_url + "/v1/accounts", headers=headers)

        return res.json()
            