

from datetime import datetime
from models.orderbook import OrderBook
from error.error import InvalidParamError
from common.const import DBConst
from database.mongodb_handler import MongoDBHandler


def get_order_order_book(created_at:str):
    client = MongoDBHandler()
    
    query = {}
    if created_at is not None:
        query['created_at'] = created_at


    find_items = client.find_items(query, db_name=DBConst.DB_NAME, collection_name=DBConst.ORDER_BOOK_COLLECTION_NAME)
    return find_items
    
    

def create_order_book(order_book):
    if order_book is None:
            raise InvalidParamError()
        
    client = MongoDBHandler()
    
    orderBook = OrderBook(
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        order_book=order_book
    )
    
    res = client.insert_item(orderBook.dict(), db_name=DBConst.DB_NAME, collection_name=DBConst.ORDER_BOOK_COLLECTION_NAME)
    return orderBook
    