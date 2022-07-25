
from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine

class BaseDao(metadata=ABCMeta):

    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass