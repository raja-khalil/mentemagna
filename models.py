# models.py - Modelos Simplificados

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager

# Função para gerar slug simples
def create_slug(text):
    """Cria slug simples sem dependências extras"""
    import re
    import unicodedata
    
    # Remover acentos
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Converter para minúsculas e substituir espaços
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    
    return text or 'post'

class User(UserMixin, db.Model):
    """Modelo de usuário para administração"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    pw_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """Define uma nova senha"""
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    """Modelo para posts do blog"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    resumo = db.Column(db.Text, nullable=True)
    imagem = db.Column(db.String(500), nullable=True)
    
    # Status e datas
    publicado = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analytics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if not self.slug and self.titulo:
            self.slug = self.generate_slug()

    def generate_slug(self):
        """Gera slug único baseado no título"""
        base_slug = create_slug(self.titulo)
        slug = base_slug
        counter = 1
        
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug

    def __repr__(self):
        return f"<Post {self.titulo}>"
    
    @property
    def reading_time(self):
        """Calcula tempo estimado de leitura"""
        words = len(self.conteudo.split())
        return max(1, round(words / 200))  # ~200 palavras por minuto

# Callback do Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))