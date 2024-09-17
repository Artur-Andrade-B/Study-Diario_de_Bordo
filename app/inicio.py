from flask import Flask,render_template,request, redirect, jsonify
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
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import base64

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def plot_cloud(wordcloud, image_path):
    plt.figure(figsize=(40,30))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()

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
            mensagem = "Texto enviado com sucesso!"
        except:
            session.rollback()
            mensagem = "Erro ao enviar o texto"
        finally:
            session.close()
    else:
        mensagem = "RA inválido"

    return render_template("diariobordo.html", ra=ra, nome=nome, mensagem=mensagem)

@app.route("/instrutor")
def acess_prof():
    return render_template("prof_login.html")

@app.route("/login_inst", methods=["POST"])
def login_prof():
    name = request.form["p_id"]
    user = session.query(Instrutor).filter_by(user_name=name).first()
    password_s = request.form["pass"]
    password_h = hash_password(password_s)
    if user.user_name == request.form["p_id"] and user.password_hash == password_h:
        return render_template("prof_area.html", user=user, nome=name)
    else:
        mensagem = "Os dados do login estão incorretos"
        return render_template("prof_login.html", mensagem = mensagem)

@app.route("/AreaDoInstrutor", methods=["POST"])
def area_prof():
    nome = request.form.get('nome')

    try:

        diariobordo_entries = session.query(Diariodebordo).all()

        if not diariobordo_entries:

            return render_template("prof_area.html", nome=nome, graph_html="<p>Sem dados para exibir.</p>")


        data = {'data_hora': [entry.data_hora.date() for entry in diariobordo_entries]}
        df_diario = pd.DataFrame(data)

        start_date = df_diario['data_hora'].min()
        end_date = datetime.now().date()  
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

        df_diario_count = df_diario.groupby('data_hora').size().reindex(all_dates, fill_value=0).reset_index(name='count')
        df_diario_count.columns = ['data_hora', 'count']

  
        num_days = len(df_diario_count)
        graph_width = min(1000 + (num_days * 5), 2000)  

        fig = px.line(df_diario_count, x='data_hora', y='count', title='Número de Entradas de Diário de Bordo por Dia')
        fig.update_layout(
            width=graph_width,
            height=500,
            xaxis_title='Data',
            yaxis_title='Número de Entradas',
            xaxis=dict(
                tickmode='linear',
                tickvals=df_diario_count['data_hora'],
                tickformat="%Y-%m-%d",
                tickangle=-45
            )         
        )
        fig.update_traces(
            line_color="purple", 
            line_width=3, 
            line_dash="dash"
            )

        graph_html = pio.to_html(fig, full_html=False)


        texto_entries = [entry.texto for entry in diariobordo_entries]
        texto_combined = ' '.join(texto_entries)
        wordcloud = WordCloud(width=500, height=500, random_state=1, background_color="grey", colormap="Blues", collocations=False, stopwords=STOPWORDS).generate(texto_combined)


        img_stream = BytesIO()
        wordcloud.to_image().save(img_stream, format='PNG')
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
        img_data = f"data:image/png;base64,{img_base64}"

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        graph_html = "<p>Erro ao gerar o gráfico.</p>"

    finally:
        session.close()

    return render_template("prof_area.html", nome=nome, graph_html=graph_html, wordcloud_image_data=img_data)

@app.route('/AcessoDoProfessor', methods=['POST'])
def listar_alunos():
    nome = request.form.get('nome')

    try:
        alunos = session.query(Aluno).all()
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos."
        return render_template('index.html', mensagem=mensagem)
    finally:
        session.close()

    return render_template('lista_alunos.html', alunos=alunos, nome=nome)

@app.route("/diario_por_ra", methods=["POST"])
def diario_por_ra():
    nome = request.form.get('nome')
    ra = request.form.get('ra')
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    nomeal = aluno.nome

    if aluno:
        diariobordo_entries = session.query(Diariodebordo).filter_by(fk_aluno_id=aluno.id).all()
        return render_template("diarioindv.html", aluno=aluno, diariobordo_entries=diariobordo_entries, nome=nome,nomeal=nomeal)
    else:
        mensagem = "Aluno não encontrado"
        return render_template("lista_alunos.html", mensagem=mensagem)
app.run(debug=True)