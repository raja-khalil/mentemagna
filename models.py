from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
import re
import unicodedata

def create_slug(text):
    if not text:
        return 'post'
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')[:100] or 'post'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    resumo = db.Column(db.Text)
    imagem = db.Column(db.String(500))
    publicado = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if not self.slug and self.titulo:
            self.slug = self.generate_unique_slug()

    def generate_unique_slug(self):
        base_slug = create_slug(self.titulo)
        slug = base_slug
        counter = 1
        
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug

    def __repr__(self):
        return f"<Post {self.titulo}>"

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager
import re
import unicodedata

def create_slug(text):
    """Gera um slug amigável para URLs a partir de um texto."""
    if not text:
        return 'post-sem-titulo'
    # Normaliza para remover acentos
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('u8')
    # Converte para minúsculas e remove caracteres especiais
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    # Substitui espaços e múltiplos hífens por um único hífen
    text = re.sub(r'[\s_-]+', '-', text)
    return text

class User(UserMixin, db.Model):
    """Modelo para usuários administradores."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    """Modelo para os posts do blog."""
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    conteudo = db.Column(db.Text, nullable=False)
    resumo = db.Column(db.String(300))
    imagem_destaque = db.Column(db.String(200)) # Caminho para a imagem
    publicado = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        if 'titulo' in kwargs and 'slug' not in kwargs:
            kwargs['slug'] = self.generate_unique_slug(kwargs['titulo'])
        super().__init__(*args, **kwargs)

    def generate_unique_slug(self, titulo):
        """Gera um slug único, adicionando um número se já existir."""
        base_slug = create_slug(titulo)
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug