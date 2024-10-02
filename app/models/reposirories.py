from base_repository import BaseRepository
from models import Aluno, Instrutor, Diariodebordo, Avaliacao, hash_password
import pandas as pd
from datetime import datetime

class AlunoRepository(BaseRepository):
    model = Aluno  # Specify the model

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def update(self, obj):
        self.session.merge(obj)  # Use merge for updates
        self.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def all(self):
        return self.session.query(self.model).all()

    def get_by_ra(self, ra):
        """Retrieve an Aluno by RA."""
        return self.session.query(self.model).filter_by(ra=ra).first()
    
    def get_last_id(self):
        """Retrieve the last ID from the Aluno table."""
        last_id = self.session.query(self.model.id).order_by(self.model.id.desc()).first()
        return (last_id[0] + 1) if last_id else None
    
    def get_nome_by_ra(self, ra):
        """Retrieve the nome of an Aluno by RA."""
        aluno = self.session.query(self.model).filter_by(ra=ra).first()
        return aluno.nome if aluno else None  # Return nome or None if not found
    def get_id_by_ra(self, ra):
        """Retrieve the ID of an Aluno by RA."""
        aluno = self.session.query(self.model).filter_by(ra=ra).first()
        return aluno.id if aluno else None  # Return nome or None if not found
    
class InstrutorRepository(BaseRepository):
    model = Instrutor

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def update(self, obj):
        self.session.merge(obj)  # Use merge for updates
        self.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def all(self):
        return self.session.query(self.model).all()
    
    def verify_password(self, username, password):
        """Verify the password for a given username."""
        user = self.session.query(self.model).filter_by(user_name=username).first()
        if user:
            hashed_password = hash_password(password)
            return user.password_hash == hashed_password
        return False

class DiariodebordoRepository(BaseRepository):
    model = Diariodebordo

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def update(self, obj):
        self.session.merge(obj)  # Use merge for updates
        self.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def all(self):
        return self.session.query(self.model).all()
    
    def get_diario_dataframe(self):
        diariobordo_entries = self.get_all_entries()
        data = {'data_hora': [entry.data_hora.date() for entry in diariobordo_entries]}
        df_diario = pd.DataFrame(data)

        # Generate date range and count entries per date
        start_date = df_diario['data_hora'].min()
        end_date = datetime.now().date()
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

        df_diario_count = df_diario.groupby('data_hora').size().reindex(all_dates, fill_value=0).reset_index(name='count')
        df_diario_count.columns = ['data_hora', 'count']
        
        return df_diario_count
    
    def get_all_entries(self):
        # Query to get all Diariodebordo entries
        return self.session.query(Diariodebordo).all()
    
    def get_combined_text_entries(self):
        diariobordo_entries = self.get_all_entries()
        texto_entries = [entry.texto for entry in diariobordo_entries]
        texto_combined = ' '.join(texto_entries)
        return texto_combined
    
    def get_text_entries_by_fk_aluno(self, aluno_id):
        return self.session.query(self.model).filter_by(fk_aluno_id=aluno_id).all()
    
    def get_combined_text_entries_by_fk_aluno(self, aluno_id):
        text_entries = self.session.query(self.model).filter_by(fk_aluno_id=aluno_id).all()
        texto_entries = [entry.texto for entry in text_entries]
        texto_combined = ' '.join(texto_entries)
        return texto_combined

class AvaliacaoRepository(BaseRepository):
    model = Avaliacao

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def update(self, obj):
        self.session.merge(obj)  # Use merge for updates
        self.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def all(self):
        return self.session.query(self.model).all()

    def get_by_ra(self,aluno_id):
        return self.session.query(self.model).filter_by(fk_aluno_id=aluno_id).first()
    
    def get_all_entries(self):
        return self.session.query(Avaliacao).all()
    
    
    def get_notas_by_ra(self, aluno_id):
        return self.session.query(self.model).filter_by(fk_aluno_id=aluno_id).all()

    