from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker

class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add(self, obj):
        """Add a new object to the session."""
        self.session.add(obj)
        self.session.commit()

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.session.query(self.model).get(obj_id)

    @abstractmethod
    def update(self, obj):
        """Update an existing object."""
        self.session.commit()

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    @abstractmethod
    def all(self):
        """Retrieve all objects."""
        return self.session.query(self.model).all()
