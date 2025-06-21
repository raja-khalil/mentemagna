#!/usr/bin/env python3
"""
Mente Magna - Aplicação Flask Simples
VERSÃO LIMPA SEM ERROS
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import re
import unicodedata

# Configuração da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentemagna.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Inicializar extensões
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Função para criar slug
def create_slug(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-') or 'post'

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Post(db.Model):
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
            base_slug = create_slug(self.titulo)
            slug = base_slug
            counter = 1
            while Post.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Formulários
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    resumo = TextAreaField('Resumo')
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    publicado = BooleanField('Publicar', default=True)
    submit = SubmitField('Salvar')

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

# Rotas Públicas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/emagna')
def emagna():
    return render_template('emagna.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject='Contato - Mente Magna',
                sender=form.email.data,
                recipients=[app.config['MAIL_USERNAME']],
                body=f"Nome: {form.nome.data}\nEmail: {form.email.data}\n\nMensagem:\n{form.mensagem.data}"
            )
            mail.send(msg)
            flash('Mensagem enviada com sucesso!', 'success')
            return redirect(url_for('contato'))
        except:
            flash('Erro ao enviar mensagem.', 'error')
    return render_template('contato.html', form=form)

@app.route('/blog')
def blog():
    posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, publicado=True).first_or_404()
    post.views += 1
    db.session.commit()
    
    recent_posts = Post.query.filter_by(publicado=True).filter(Post.id != post.id).order_by(Post.data_criacao.desc()).limit(6).all()
    return render_template('post.html', post=post, recent_posts=recent_posts)

# Rotas de Autenticação
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Credenciais inválidas', 'error')
    return render_template('auth/login.html', form=form)

@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rotas Admin
@app.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    stats = {
        'total_posts': len(posts),
        'published_posts': len([p for p in posts if p.publicado]),
        'draft_posts': len([p for p in posts if not p.publicado]),
        'total_views': sum(p.views for p in posts),
        'this_week_posts': len([p for p in posts if (datetime.now() - p.data_criacao).days <= 7])
    }
    return render_template('admin/dashboard.html', posts=posts, stats=stats)

@app.route('/admin/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.imagem.data:
            f = form.imagem.data
            if f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            resumo=form.resumo.data,
            imagem=f'/static/uploads/{filename}' if filename else None,
            publicado=form.publicado.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/editor.html', form=form, legend="Novo Post")

@app.route('/admin/editar/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.conteudo.data
        post.resumo = form.resumo.data
        post.publicado = form.publicado.data
        
        if form.imagem.data and form.imagem.data.filename:
            filename = secure_filename(form.imagem.data.filename)
            form.imagem.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.imagem = f'/static/uploads/{filename}'
        
        db.session.commit()
        flash('Post atualizado!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/editor.html', form=form, post=post, legend="Editar Post")

@app.route('/admin/deletar/<int:post_id>', methods=['POST'])
@login_required
def deletar_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deletado!', 'success')
    return redirect(url_for('admin_dashboard'))

# Criar tabelas e dados iniciais
with app.app_context():
    db.create_all()
    
    # Criar admin se não existir
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@mentemagna.com')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado (admin/123456)")

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    print("🚀 Mente Magna rodando em http://localhost:5000")
    print("👤 Admin: http://localhost:5000/auth/login (admin/123456)")
    app.run(debug=True)