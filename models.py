# models.py - ATUALIZADO com sistema de categorias
from datetime import datetime
from slugify import slugify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager

# Tabela de associação para many-to-many entre Post e Category
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class Category(db.Model):
    """Modelo para categorias do blog"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), default='#007bff')  # Cor hex para display
    icon = db.Column(db.String(50), default='📝')  # Emoji ou classe de ícone
    seo_keywords = db.Column(db.Text, nullable=True)  # Keywords específicas da categoria
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)  # Para ordenação
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com posts
    posts = db.relationship('Post', secondary=post_categories, 
                           back_populates='categories', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.name:
            self.slug = slugify(self.name)
    
    @property
    def post_count(self):
        """Retorna número de posts publicados nesta categoria"""
        return self.posts.filter_by(publicado=True).count()
    
    def __repr__(self):
        return f"<Category {self.name}>"

class Post(db.Model):
    """Modelo para posts do blog - ATUALIZADO"""
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
    
    # Novos campos para SEO
    meta_description = db.Column(db.String(160), nullable=True)  # Meta description específica
    keywords = db.Column(db.Text, nullable=True)  # Keywords específicas do post
    
    # Campos para analytics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    
    # Relacionamento com categorias
    categories = db.relationship('Category', secondary=post_categories, 
                                back_populates='posts', lazy='subquery')
    
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
    def primary_category(self):
        """Retorna a primeira categoria do post"""
        return self.categories[0] if self.categories else None
    
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
    """Modelo de usuário - SEM ALTERAÇÕES"""
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

# Função para criar categorias padrão
def create_default_categories():
    """Cria categorias padrão do sistema"""
    default_categories = [
        {
            'name': 'Inteligência Artificial',
            'description': 'Artigos sobre IA, Machine Learning, Deep Learning e ChatGPT',
            'color': '#e74c3c',
            'icon': '🤖',
            'seo_keywords': 'inteligência artificial, machine learning, deep learning, chatgpt, ia, algoritmos'
        },
        {
            'name': 'Programação',
            'description': 'Tutoriais de programação, linguagens e desenvolvimento',
            'color': '#3498db',
            'icon': '💻',
            'seo_keywords': 'programação, python, javascript, desenvolvimento, código, algoritmos'
        },
        {
            'name': 'Web Development',
            'description': 'Desenvolvimento web, frontend, backend e frameworks',
            'color': '#2ecc71',
            'icon': '🌐',
            'seo_keywords': 'desenvolvimento web, frontend, backend, html, css, javascript, react'
        },
        {
            'name': 'Mobile',
            'description': 'Desenvolvimento de aplicativos móveis',
            'color': '#9b59b6',
            'icon': '📱',
            'seo_keywords': 'desenvolvimento mobile, android, ios, react native, flutter'
        },
        {
            'name': 'Cloud & DevOps',
            'description': 'Cloud computing, DevOps, Docker e infraestrutura',
            'color': '#f39c12',
            'icon': '☁️',
            'seo_keywords': 'cloud computing, devops, docker, kubernetes, aws, azure'
        },
        {
            'name': 'Ferramentas',
            'description': 'Ferramentas úteis, calculadoras e utilitários',
            'color': '#1abc9c',
            'icon': '🔧',
            'seo_keywords': 'ferramentas online, calculadora, utilitários, produtividade'
        }
    ]
    
    for cat_data in default_categories:
        existing = Category.query.filter_by(slug=slugify(cat_data['name'])).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("✅ Categorias padrão criadas!")

# Função para migrar posts existentes
def migrate_existing_posts():
    """Adiciona categoria padrão para posts sem categoria"""
    from extensions import db
    
    default_category = Category.query.filter_by(slug='programacao').first()
    if not default_category:
        return
    
    posts_without_category = Post.query.filter(~Post.categories.any()).all()
    
    for post in posts_without_category:
        post.categories.append(default_category)
    
    db.session.commit()
    print(f"✅ {len(posts_without_category)} posts migrados para categoria padrão!")