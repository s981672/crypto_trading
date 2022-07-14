

from datetime import datetime
from error.error import InvalidParamError
from common.const import DBConst
from database.mongodb_handler import MongoDBHandler
from models.user import User


def get_user(user_id : str = None):
    client = MongoDBHandler()
    
    query = {}
    if user_id is not None:
        query['user_id'] = user_id

    find_items = client.find_items(query, db_name=DBConst.DB_NAME, collection_name=DBConst.USER_COLLECTION_NAME)
    return find_items
    
    

def create_user(user_id, email, phone, budget):
    if user_id is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    user = User(
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        user_id=user_id,
        email=email,
        phone=phone,
        budget=budget
    )
    
    res = client.insert_item(user.dict(), db_name=DBConst.DB_NAME, collection_name=DBConst.USER_COLLECTION_NAME)
    return res
    
    
def update_user(user_id, email:str= None, phone:str = None, budget:str= None):
    if user_id is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    update_value = {
        "$set" : {
            "updated_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    }
    if email is not None:
        update_value['$set']['email'] = email
    if phone is not None:
        update_value['$set']['phone'] = phone
    if budget is not None:
        update_value['$set']['email'] = budget
        
    
    condition = {
        "user_id" : user_id,
    }
    
    client.update_item(update_value, condition, db_name=DBConst.DB_NAME, collection_name=DBConst.USER_COLLECTION_NAME)    