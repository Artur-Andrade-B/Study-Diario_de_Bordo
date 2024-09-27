from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker

class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add(self, obj):
        pass


    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def update(self, obj):
        pass


    @abstractmethod
    def delete(self, obj_id):
        pass


    @abstractmethod
    def all(self):
        pass
