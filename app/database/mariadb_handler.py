from typing import Any, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from error.error import InvalidParamError

class MariadbHandler():
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
        
        session.add(item)
        session.commit()

    def insert_items(self, items):
        if items is None:
            raise Exception()
        
        session = self.__get_session()
        
        session.add_all(items)
        session.commit()
    
    def find_items(self, entities, condition=None):
        if condition is None:
            condition = {}
            
        session = self.__get_session()
        
        query_result:List[entities] = session.query(entities).filter_by(**condition).all()

        return query_result
        
    def delete_item(self, item):
        if item is None:
            raise Exception()
        
        session = self.__get_session()
        session.delete(item)
        session.commit()
    
        
    def update_item(self, condition=None, item=None):
        if condition is None or item is None:
            raise Exception()
        
        session = self.__get_session()
        session.query(item.__class__).filter_by(**condition).update(item.to_dict())
        session.commit()
