

from abc import ABCMeta, abstractmethod


class DBHandler(metaclass=ABCMeta):
    
    @abstractmethod
    def insert_item(self):
        pass
    
    @abstractmethod
    def insert_items(self):
        pass
    
    @abstractmethod
    def find_items(self):
        pass

    @abstractmethod
    def find_item(self):
        pass
    
    @abstractmethod
    def delete_item(self):
        pass
    
    @abstractmethod
    def update_item(self):
        pass