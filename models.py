from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager
import re
import unicodedata
from sqlalchemy.event import listen

def create_slug(text):
    if not text:
        return 'post-sem-titulo'
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s_-]+', '-', text)

class User(UserMixin, db.Model):
    # Definindo explicitamente o nome da tabela como 'users' (plural)
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    pw_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Post(db.Model):
    # Definindo explicitamente o nome da tabela como 'posts' (plural)
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

def before_post_save(mapper, connection, target):
    target.generate_unique_slug()

listen(Post, 'before_insert', before_post_save)
listen(Post, 'before_update', before_post_save)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))