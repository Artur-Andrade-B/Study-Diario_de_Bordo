import hashlib
import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Instrutor:
    def __init__(self, user_name, password_hash):
        self.user_name = user_name
        self.password_hash = password_hash
    
class Aluno:
    def __init__(self, ra, nome, tempo_de_estudo, renda_media_salarial, id):
        self.ra = ra
        self.nome = nome
        self.tempo_de_estudo = tempo_de_estudo
        self.renda_media_salarial = renda_media_salarial
        self.id = id

class Diariodebordo:
    def __init__(self, texto, data_hora, fk_aluno_id):
        self.texto = texto
        self.data_hora = data_hora
        self.fk_aluno_id = fk_aluno_id