# models.py - Versão simplificada
from datetime import datetime
from slugify import slugify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager

class Post(db.Model):
    """Modelo para posts do blog"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    resumo = db.Column(db.Text, nullable=True)
    conteudo = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    publicado = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos para SEO
    meta_description = db.Column(db.String(160), nullable=True)
    keywords = db.Column(db.Text, nullable=True)
    
    # Campos para analytics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Se não foi fornecido slug, gera a partir do título
        if not self.slug and self.titulo:
            self.slug = slugify(self.titulo)
        # Se não há resumo, extrai dos primeiros 200 caracteres do conteúdo
        if not self.resumo:
            plain = (self.conteudo or "").replace('<', '').replace('>', '')
            self.resumo = (plain[:200] + '...') if len(plain) > 200 else plain
    
    @property
    def reading_time(self):
        """Estima tempo de leitura em minutos"""
        words = len(self.conteudo.split())
        return max(1, round(words / 200))  # ~200 palavras por minuto
    
    def increment_views(self):
        """Incrementa contador de visualizações"""
        self.views += 1
        db.session.commit()
    
    def __repr__(self):
        return f"<Post {self.slug}>"

class User(UserMixin, db.Model):
    """Modelo de usuário"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pw_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# callback para Flask-Login
@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))