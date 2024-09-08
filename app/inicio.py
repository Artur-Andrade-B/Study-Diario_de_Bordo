from flask import Flask,render_template,request, redirect
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import pymysql
import urllib.parse
from aluno import Aluno
from instrutor import Instrutor
from diariobordo import Diariodebordo
import random
import pandas as pd
import hashlib
import getpass
from datetime import datetime, timezone

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

user = "root"
password = urllib.parse.quote_plus("0413")

host = "localhost"
database = "projetodiario"

connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

base = automap_base(metadata=metadata)
base.prepare()

Aluno = base.classes.aluno
Instrutor = base.classes.instrutor
Diariodebordo = base.classes.diariobordo 

Session = sessionmaker(bind=engine)
session = Session()


app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/instrutor")
def acess_pro():
    return render_template("prof_login.html")

@app.route("/login_inst", methods=["POST"])
def login_prof():
    name = request.form["p_id"]
    user = session.query(Instrutor).filter_by(user_name=name).first()
    password_s = request.form["pass"]
    password_h = hash_password(password_s)
    if user.user_name == request.form["p_id"] and user.password_hash == password_h:
        return redirect("/AcessoDoProfessor")
    else:
        mensagem = "Os dados do login estão incorretos"
        return render_template("prof_login.html", mensagem = mensagem)


@app.route("/registrar")
def realizar_cadastro():
    return render_template("novoaluno.html")

@app.route("/cadastro", methods=["POST"])
def register_aluno():
    ra = request.form["ra"]
    if session.query(Aluno).filter_by(ra=ra).first():
        mensagem = "o ra informado já existe"
        return render_template("index.html", mensagem = mensagem)

    else:
        nome = request.form["nome"]
        rms = float(request.form["renda_media_salarial"])
        ts = int(request.form["tempo_de_estudo"])
        aluno = Aluno(ra = ra, nome = nome, tempo_de_estudo = ts, renda_media_salarial = rms)

        try:
            session.add(aluno)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        mensagem = "cadastro efetuado com sucesso"
        return render_template("index.html", msgbanco = mensagem)

@app.route("/login", methods=["POST"])
def login_ra():
    ra = request.form["ra"]
    
    if session.query(Aluno).filter_by(ra=ra).first():
        usuario = session.query(Aluno).filter_by(ra=ra).first()
        nome = usuario.nome
        return render_template("diariobordo.html", ra = ra, nome = nome)
       
    else:
        mensagem = "o ra está invalido"
        return render_template("index.html", mensagem = mensagem)

@app.route("/submit_diario", methods=["POST"])
def submit_diario():
    ra = request.form["ra"]
    nome = request.form["nome"]
    texto = request.form["texto"]
    data_hora = datetime.now(timezone.utc)
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    fk = aluno.id

    if aluno:
        diario = Diariodebordo(texto=texto, data_hora=data_hora, fk_aluno_id=fk)
        try:
            session.add(diario)
            session.commit()
            mensagem = "Texto enviado com sucesso"
        except:
            session.rollback()
            mensagem = "Erro ao enviar o texto"
        finally:
            session.close()
    else:
        mensagem = "RA inválido"

    return render_template("diariobordo.html", ra=ra, nome=nome, mensagem=mensagem)

@app.route('/AcessoDoProfessor', methods=['GET'])
def listar_alunos():
    try:
        alunos = session.query(Aluno).all()
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos."
        return render_template('index.html', mensagem=mensagem)
    finally:
        session.close()

    return render_template('lista_alunos.html', alunos=alunos)
app.run()