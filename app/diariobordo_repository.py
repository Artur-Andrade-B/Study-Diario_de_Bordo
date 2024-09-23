from base_repository import BaseRepository
from models import Diariodebordo

class DiarioRepository(BaseRepository):
    def __init__(self):
        super().__init__(Diariodebordo)

    def get_all(self, session):
        return session.query(self.model).all()

    def get_by_id(self, session, id):
        return session.query(self.model).filter_by(id=id).first()

    def add(self, session, instance):
        instance.save(session)

    def delete(self, session, instance):
        instance.delete(session)
