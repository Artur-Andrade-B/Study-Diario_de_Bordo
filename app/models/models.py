import hashlib
import getpass
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from base_model import BaseModel

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Instrutor(BaseModel):
    __tablename__ = 'instrutor'

    id = Column(Integer, primary_key=True)  # Ensure this column is defined
    user_name = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)

    def __init__(self, user_name, password_hash):
        self.user_name = user_name
        self.password_hash = password_hash
    
class Aluno(BaseModel):
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True)  # Primary key
    ra = Column(String(8), unique=True, nullable=False)
    nome = Column(String(50), nullable=True)  # Adjusting to match your SQL
    tempo_de_estudo = Column(Integer, nullable=False)  # Adjusted as not nullable
    renda_media_salarial = Column(Integer, nullable=True)

    diarios = relationship('Diariodebordo', back_populates='aluno')
    notas = relationship('Avaliacao', back_populates='aluno')

    def __init__(self, ra, nome, tempo_de_estudo, renda_media_salarial, id):
        self.ra = ra
        self.nome = nome
        self.tempo_de_estudo = tempo_de_estudo
        self.renda_media_salarial = renda_media_salarial
        self.id = id

class Diariodebordo(BaseModel):
    id = Column(Integer, primary_key=True)
    texto = Column(Text, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    fk_aluno_id = Column(Integer, ForeignKey('aluno.id'))

    aluno = relationship('Aluno', back_populates='diarios')
    __tablename__ = 'diariobordo'
    def __init__(self, texto, data_hora, fk_aluno_id):
        self.texto = texto
        self.data_hora = data_hora
        self.fk_aluno_id = fk_aluno_id

class Avaliacao(BaseModel):
    id = Column(Integer, primary_key=True)
    nota1 = Column(Integer)
    nota2 = Column(Integer)
    nota3 = Column(Integer)
    nota4 = Column(Integer)
    fk_aluno_id = Column(Integer, ForeignKey('aluno.id'))

    aluno = relationship('Aluno', back_populates='notas')
    __tablename__ = 'avaliacao'
    def __init__(self,nota1=0,nota2=0,nota3=0,nota4=0,fk_aluno_id=0):
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.nota4 = nota4
        self.fk_aluno_id = fk_aluno_id

