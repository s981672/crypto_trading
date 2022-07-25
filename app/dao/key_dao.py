

from datetime import datetime

from pytz import timezone
from error.error import InvalidParamError
from common.const import DBConst
from database.mongodb_handler import MongoDBHandler
from models.api_key import ApiKey


def get_api_key(user_id : str = None, exchange : str = None):
    client = MongoDBHandler()
    
    query = {}
    if user_id is not None:
        query['user_id'] = user_id
    if exchange is not None:
        query['exchange'] = exchange

    find_items = client.find_items(query, db_name=DBConst.DB_NAME, collection_name=DBConst.API_KEY_COLLECTION_NAME)
    return find_items
    
    

def create_api_key(user_id, exchange, access, secret):
    if user_id is None or exchange is None or access is None or secret is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    api_key = ApiKey(
        created_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        user_id=user_id,
        exchange=exchange,
        access=access,
        secret=secret
    )
    
    res = client.insert_item(api_key.dict(), db_name=DBConst.DB_NAME, collection_name=DBConst.API_KEY_COLLECTION_NAME)
    return res
    
    
def update_api_key(user_id, exchange, api_key):
    if user_id is None or exchange is None or api_key is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    update_value = {
        "$set" : {
            "updated_at" : datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
            'access' : api_key['access'],
            "secret" : api_key['secret']
        }
    }
    
    condition = {
        "user_id" : api_key["user_id"],
        'exchange' : api_key['exchange']
    }
    
    client.update_item(update_value, condition, db_name=DBConst.DB_NAME, collection_name=DBConst.API_KEY_COLLECTION_NAME)    