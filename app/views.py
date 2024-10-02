from templates import *
from flask import Flask,render_template,request, redirect, jsonify
from datetime import datetime, timezone
from models import *
from graphy import Wordy, Ploty
from singleton import SingletonSession
from reposirories import AlunoRepository, InstrutorRepository, DiariodebordoRepository, AvaliacaoRepository
session = SingletonSession.get_instance()
aluno_repository = AlunoRepository(session)
diario_repository = DiariodebordoRepository(session)
instrutor_repository = InstrutorRepository(session)
avaliacao_repository = AvaliacaoRepository(session)
import logging

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
    if aluno_repository.get_by_ra(ra):
        msgbanco = "o ra informado já existe"
        return render_template("index.html", msgbanco = msgbanco)

    else:
        nome = request.form["nome"]
        rms = float(request.form["renda_media_salarial"])
        ts = int(request.form["tempo_de_estudo"])
        lid = aluno_repository.get_last_id()
        aluno = Aluno(id = lid, ra = ra, nome = nome, tempo_de_estudo = ts, renda_media_salarial = rms)

        try:
            aluno_repository.add(aluno)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        mensagem = "cadastro efetuado com sucesso"
        return render_template("index.html", mensagem = mensagem)

@app.route("/login", methods=["POST"])
def login_ra():
    ra = request.form["ra"]
    
    if aluno_repository.get_by_ra(ra):
        nome = aluno_repository.get_nome_by_ra(ra)
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
    fk = aluno_repository.id

    if fk:
        diario = Diariodebordo(texto=texto, data_hora=data_hora, fk_aluno_id=fk)
        try:
            diario_repository.add(diario)
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

    username = request.form["p_id"]
    password = request.form["pass"]

    if instrutor_repository.verify_password(username, password):
        try:
            
            df_diario_count = diario_repository.get_diario_dataframe()

            num_days = len(df_diario_count)
            graph_width = min(1000 + (num_days * 5), 2000)

            g_l = Ploty(df_diario_count, "data_hora", graph_width, "count",
                        "Número de diarios de bordo preenchidos pela turma")
            g_l.create_fig()
            graph_html = g_l.get_ht()

            texto_combined = diario_repository.get_combined_text_entries()

            w_c = Wordy(texto_combined)
            w_c.create_wordcloud()
            wc = w_c.get_wc()
            

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            graph_html = "<p>Erro ao gerar o gráfico.</p>"

        finally:
            session.close()
            return render_template("prof_area.html", user=username, nome=username, graph_html=graph_html, wordcloud_image_data=wc)
    else:
        mensagem = "Os dados do login estão incorretos"
        return render_template("prof_login.html", mensagem=mensagem)

@app.route("/AreaDoInstrutor", methods=["POST"])
def area_prof():
    nome = request.form.get('nome')

    try:

        df_diario_count = diario_repository.get_diario_dataframe()

        num_days = len(df_diario_count)
        graph_width = min(1000 + (num_days * 5), 2000)

        g_l = Ploty(df_diario_count, "data_hora", graph_width, "count",
                    "Número de diarios de bordo preenchidos pela turma")
        g_l.create_fig()
        graph_html = g_l.get_ht()

        texto_combined = diario_repository.get_combined_text_entries()

        w_c = Wordy(texto_combined)
        w_c.create_wordcloud()
        wc = w_c.get_wc()
            
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        graph_html = "<p>Erro ao gerar o gráfico.</p>"

    finally:
        session.close()
        return render_template("prof_area.html", nome=nome, graph_html=graph_html, wordcloud_image_data=wc)


@app.route('/AcessoDoProfessor', methods=['POST'])
def listar_alunos():
    nome = request.form.get('nome')

    try:
        alunos = aluno_repository.all()
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
    aluno = aluno_repository.get_by_ra(ra)

    try:
        if aluno:
            nomeal = aluno.nome
            diariobordo_entries = diario_repository.get_text_entries_by_fk_aluno(aluno.id)
            all_texts = diario_repository.get_combined_text_entries_by_fk_aluno(aluno.id)
                
            w_c_i = Wordy(all_texts,w=300,h=300,cm="plasma")
            w_c_i.create_wordcloud()
            

            return render_template("diarioindv.html", aluno=aluno, diariobordo_entries=diariobordo_entries, nome=nome,
                                nomeal=nomeal, wordcloud_image_data=w_c_i.get_wc())
        else:
            session.rollback()
            alunos = aluno_repository.all()
            mensagem = "Aluno não encontrado"
            return render_template("lista_alunos.html", mensagem=mensagem, alunos=alunos)
    except:
        alunos = aluno_repository.all()
        mensagem = "Aluno não tem nenhum diario de bordo preenchido"
        return render_template("lista_alunos.html", mensagem=mensagem, alunos=alunos)
    finally:
        session.close()

@app.route("/notas",methods=["POST","GET"])
def listar_notas():
    nome = request.form.get('nome')
        
    try:
        alunos = aluno_repository.all()
        notas_data = {aluno.id: avaliacao_repository.get_notas_by_ra(aluno.id) for aluno in alunos}
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos."
        return render_template('index.html', mensagem=mensagem)
    finally:
        session.close()

    return render_template('prof_notas.html', alunos=alunos, nome=nome,notas_data=notas_data)


@app.route('/update_notas', methods=['POST', "GET"])
def update_notas():
    data = request.get_json()
    logging.debug(f"Incoming data: {data}")
    print(data)
    if 'ra' not in data:
        return jsonify({'error': 'RA is required'}), 400

    ra = data['ra']
    ra = int(ra)
    grades_to_update = {key: value for key, value in data.items() if key != 'ra'}
    k = [*grades_to_update]
    key = k[0]
    val = grades_to_update.get(key)
    val = int(val)


    try:
        aluno = session.query(Aluno).filter_by(ra=ra).first()
        if not aluno:
            return jsonify({'error': 'Student not found'}), 404
        
        avaliacao = session.query(Avaliacao).filter_by(fk_aluno_id=aluno.id).first()

        if not avaliacao:
            match key:
                case "nota1":
                    aval = Avaliacao(nota1=val, fk_aluno_id=aluno.id)
                case "nota2":
                    aval = Avaliacao(nota2=val, fk_aluno_id=aluno.id)
                case "nota3":
                    aval = Avaliacao(nota3=val, fk_aluno_id=aluno.id)
                case "nota4":
                    aval = Avaliacao(nota4=val, fk_aluno_id=aluno.id)                                                
            
            avaliacao_repository.add(aval)
            session.commit()
        else:
            c_aval = avaliacao_repository.get_by_ra(aluno.id)
            match key:
                case "nota1":
                    aval = Avaliacao(nota1=val, nota2=c_aval.nota2,
                                     nota3=c_aval.nota3, nota4=c_aval.nota4,
                                     fk_aluno_id=aluno.id)
                case "nota2":
                    aval = Avaliacao(nota2=val, fk_aluno_id=aluno.id)
                case "nota3":
                    aval = Avaliacao(nota3=val, fk_aluno_id=aluno.id)
                case "nota4":
                    aval = Avaliacao(nota4=val, fk_aluno_id=aluno.id) 
            avaliacao_repository.update(aval)
            session.commit()
            return jsonify({'message': 'Grades updated successfully'}), 200

    except Exception as e:
        session.rollback()
        logging.error(f"Error updating grades: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close
    return jsonify({'message': 'Grades updated successfully'}), 250


