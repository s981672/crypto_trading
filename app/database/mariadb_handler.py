import logging
from typing import Any, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from database.base_handler import DBHandler

from error.error import InvalidParamError

logger = logging.getLogger('sLogger')

class MariadbHandler(DBHandler):
    def __init__(self, hostName:str = "127.0.0.1"):
        self.engine = create_engine("mariadb+mariadbconnector://bml_admin:Wjswlgus2022!@localhost:3306/bml")
        self.conn = self.engine.connect()
        # self.engine = create_engine(f"mysql+mysqldb://root:Wjswlgus2022!@127.0.0.1:3306/bml", encoding='utf-8')
        # self.conn = self.engine.connect()

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
            
    
    def __get_session(self):
        
        return self.session        

    def insert_item(self, item):
        if item is None:
            raise Exception()
        
        session = self.__get_session()
        
        logger.info(f"[DB] INSERT ITEM : {item}")
        session.add(item)
        session.commit()

    def insert_items(self, items):
        if items is None:
            raise Exception()
        
        session = self.__get_session()
        
        logger.info(f"[DB] INSERT ITEMS : {items}")
        session.add_all(items)
        session.commit()
    
    def find_item(self, entities, condition=None):
        logger.info(f"[DB] FIND ITEM. condtion :{condition}")

        query_result = self.find_items(entities, condition)
        if len(query_result) > 0 :
            return query_result[0]
    
    def find_items(self, entities, condition=None):
        logger.info(f"[DB] FIND ITEMs. condtion :{condition}")

        if condition is None:
            condition = {}
            
        session = self.__get_session()
        
        query_result:List[entities] = session.query(entities).filter_by(**condition).all()

        return query_result
        
    def delete_item(self, item):
        logger.info(f"[DB] DELETE ITEM : {item}")

        if item is None:
            raise Exception()
        
        session = self.__get_session()
        session.delete(item)
        session.commit()
    
        
    def update_item(self, condition=None, item=None):
        logger.info(f"[DB] UPDATE ITEM. condition:{condition}, item: {item}")

        if condition is None or item is None:
            raise Exception()
        
        session = self.__get_session()
        session.query(item.__class__).filter_by(**condition).update(item.to_dict())
        session.commit()
