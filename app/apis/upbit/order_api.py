
from apis.abstract_api import AbstractOrder
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

class OrderApi(AbstractOrder):
    access_key = 'DMbAWg9xO9ObiEvBpn0RfCLxJ31d1xsqhdoodK7P'
    secret_key = 'fkUgm0agMZGO2efsSgxGYhXSRxYDzVD32ZdbbBnt'
    server_url = 'https://api.upbit.com'
    
    def order(self, param):
        print('Upbit Order')
        
    def buy(self, param):
        query = param.toJson()
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)

        return res.json()
    
    def orders_chance(self, market):
        query = {
            'market': market
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/orders/chance", params=query, headers=headers)

        return res.json()
        