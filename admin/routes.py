# admin/routes.py
import os, uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Post
from forms import PostForm

admin_bp = Blueprint('admin', __name__, template_folder='templates')
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','mp4'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(fn):
    ext = fn.rsplit('.',1)[1].lower()
    return '.' in fn and ext in ALLOWED_EXTENSIONS

@admin_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    if f and allowed_file(f.filename):
        name = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, name)
        f.save(path)
        url = url_for('static', filename=f'uploads/{name}')
        return {'url': url}
    return {'error': 'Formato inválido'}, 400

@admin_bp.route('/')
def dashboard():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('dashboard.html', posts=posts)

@admin_bp.route('/novo', methods=['GET','POST'])
def novo_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.imagem.data:
            f = form.imagem.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            imagem=f'/static/uploads/{filename}' if filename else None,
            data_criacao=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        flash('Post publicado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('editor.html', form=form)
