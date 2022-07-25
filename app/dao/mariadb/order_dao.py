

from datetime import datetime

from pytz import timezone
from error.error import InvalidParamError
from common.const import DBConst
from database.mongodb_handler import MongoDBHandler
from models.order import OrderInfo, Order


def get_order(user_id: str = None , strategy_id: str = None, uuid: str = None, state: str = None):
    client = MongoDBHandler()
    
    query = {}
    if user_id is not None:
        query['user_id'] = user_id
    if strategy_id is not None:
        query['strategy_id'] = strategy_id
    if uuid is not None:
        query['uuid'] = uuid
    if state is not None:
        query['state'] = state


    find_items = client.find_items(query, db_name=DBConst.DB_NAME, collection_name=DBConst.ORDERS_COLLECTION_NAME)
    return find_items
    
    

def create_order(user_id, strategy_id, order_info, expected_price:str=None):
    if user_id is None or strategy_id is None or order_info is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    order = Order(
        created_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        user_id=user_id,
        strategy_id=strategy_id,
        uuid=order_info['uuid'],
        order=order_info,
        expected_price=expected_price,
        state="wait"
    )
    
    res = client.insert_item(order.dict(), db_name=DBConst.DB_NAME, collection_name=DBConst.ORDERS_COLLECTION_NAME)
    return order
    
    
def update_order(user_id, strategy_id, order, state):
    if user_id is None or strategy_id is None or order is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    update_value = {
        "$set" : {
            "updated_at" : datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
            "order" : order
        }
    }
    
    if state is not None:
        update_value['$set']['state'] = state
    
    condition = {
        "uuid" : order["uuid"]
    }
    
    client.update_item(update_value, condition, db_name=DBConst.DB_NAME, collection_name=DBConst.ORDERS_COLLECTION_NAME)    