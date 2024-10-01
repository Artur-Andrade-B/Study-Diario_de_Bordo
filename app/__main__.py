import sys
sys.path.insert(0,"c:\\Users\\ead\\Documents\\Artur\\Study-Diario_de_Bordo\\app\\models")
sys.path.insert(0,"c:\\Users\\ead\\Documents\\Artur\\Study-Diario_de_Bordo\\app\\templates")


from flask import Flask,render_template,request, redirect, jsonify
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from models import Aluno, Instrutor, Diariodebordo
import urllib.parse

user = "root"
password = urllib.parse.quote_plus("senai@123")

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
# Import views after initializing the app
from views import *  # Ensure views are imported after app is created

app.run(debug=True)
