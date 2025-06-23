from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager
import re
import unicodedata
from sqlalchemy.event import listen

def create_slug(text):
    if not text:
        return 'sem-titulo'
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s_-]+', '-', text)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    pw_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    conteudo = db.Column(db.Text, nullable=False)
    resumo = db.Column(db.String(300))
    imagem = db.Column(db.String(200))
    publicado = db.Column(db.Boolean, default=False, nullable=False, index=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def generate_unique_slug(self):
        base_slug = create_slug(self.titulo)
        slug = base_slug
        counter = 1
        while Post.query.filter(Post.id != self.id).filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

# NOVO MODELO DE PRODUTO
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, default='Geral')
    short_description = db.Column(db.String(300))
    # Note que a descrição completa agora é um campo no DB, não em um arquivo HTML
    full_description_html = db.Column(db.Text) 
    image_file = db.Column(db.String(200), nullable=False)
    amazon_link = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False, index=True) # Para o destaque na home
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def generate_unique_slug(self):
        base_slug = create_slug(self.name)
        slug = base_slug
        counter = 1
        while Product.query.filter(Product.id != self.id).filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

listen(Post, 'before_insert', lambda m, c, t: t.generate_unique_slug())
listen(Post, 'before_update', lambda m, c, t: t.generate_unique_slug())

# Adiciona o listener para o novo modelo Product
listen(Product, 'before_insert', lambda m, c, t: t.generate_unique_slug())
listen(Product, 'before_update', lambda m, c, t: t.generate_unique_slug())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))