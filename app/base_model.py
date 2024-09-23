from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # This class will not create a table

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
        
class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self, session):
        return session.query(self.model).all()

    def get_by_id(self, session, id):
        return session.query(self.model).filter_by(id=id).first()

    def add(self, session, instance):
        instance.save(session)

    def delete(self, session, instance):
        instance.delete(session)
