

from datetime import datetime

from pytz import timezone
from models.strategy import Strategy
from error.error import InvalidParamError
from common.const import DBConst
from database.mongodb_handler import MongoDBHandler
from models.user import User


def get_strategy(user_id : str = None, strategy_id:str = None):
    client = MongoDBHandler()
    
    query = {}
    if user_id is not None:
        query['user_id'] = user_id
    if strategy_id is not None:
        query['strategy_id'] = strategy_id

    find_items = client.find_items(query, db_name=DBConst.DB_NAME, collection_name=DBConst.STRATEGY_COLLECTION_NAME)
    return find_items
    
    

def create_strategy(user_id, strategy_id, weight, budget, volume):
    if user_id is None or strategy_id is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    strategy = Strategy(
        strategy_id=strategy_id,
        created_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        user_id=user_id,
        weight=weight,
        budget=budget,
        volume=volume        
    )
    
    res = client.insert_item(strategy.dict(), db_name=DBConst.DB_NAME, collection_name=DBConst.STRATEGY_COLLECTION_NAME)
    return res
    
    
def update_strategy(user_id, strategy_id, weight:int = None, budget:str = None, volume:str = None, locked_volume:str = None):
    if user_id is None or strategy_id is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    update_value = {
        "$set" : {
            "updated_at" : datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S'),
        }
    }
    if weight is not None:
        update_value['$set']['weight'] = weight
    if budget is not None:
        update_value['$set']['budget'] = budget
    if volume is not None:
        update_value['$set']['volume'] = volume
    if locked_volume is not None:
        update_value['$set']['locked_volume'] = locked_volume
        
    
    condition = {
        "user_id" : user_id,
        "strategy_id" : strategy_id
    }
    
    client.update_item(update_value, condition, db_name=DBConst.DB_NAME, collection_name=DBConst.STRATEGY_COLLECTION_NAME)    