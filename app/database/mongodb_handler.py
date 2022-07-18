
from pymongo import MongoClient
from pymongo.cursor import CursorType
from common.const import DBConst

from database.base_handler import DBHandler


class MongoDBHandler(DBHandler):
    
    def __init__(self, host="localhost/", db_name=None, collection_name=None):
        self._db_client = MongoClient(f"mongodb://{host}", port={DBConst.DB_PORT})
        
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None and self._db is not None:
            self._collection = self._db[collection_name]
        
    #TODO
    # 초기에 DB나 Colletion이 없는 경우에 생성하는 부분이 필요할 것 같음.
    
    def insert_item(self, item, db_name=None, collection_name=None):
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        res = self._collection.insert_one(item)
        return res

    def insert_items(self, items, db_name=None, collection_name=None):
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        res = self._collection.insert_many(items)
        return res
    
    def find_items(self, condition=None, db_name=None, collection_name=None):
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        res = self._collection.find(condition, cursor_type=CursorType.EXHAUST)
        return res

    def find_item(self, condition=None, db_name=None, collection_name=None):
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        print(condition,db_name, collection_name )
        res = self._collection.find_one(condition)
        return res
        
    
    def delete_item(self, condition=None, db_name=None, collection_name=None):
        if condition is None:
            raise Exception("No Condition")
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        res = self._collection.delete_one(condition)
        return res
        
    def update_item(self, update_data=None, condition=None, db_name=None, collection_name=None):
        if condition is None:
            raise Exception("No Condition")
        if update_data is None:
            raise Exception("No Update Data")
        if db_name is not None:
            self._db = self._db_client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        res = self._collection.update_one(filter=condition, update=update_data)
        return res
