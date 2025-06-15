 # models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200))  # caminho da imagem
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

