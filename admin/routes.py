import os
from flask import (Blueprint, render_template, redirect, url_for, flash,
                   request, jsonify, current_app)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models import Post
from forms import PostForm

# O template_folder aponta para a pasta de templates dentro do blueprint 'admin'
admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
@login_required
def dashboard():
    """Exibe o painel com todos os posts."""
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('dashboard.html', posts=posts, title="Dashboard")

@admin_bp.route('/post/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
    """Página para criar um novo post."""
    form = PostForm()
    if form.validate_on_submit():
        novo_post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            resumo=form.resumo.data,
            publicado=form.publicado.data
        )
        # O slug é gerado automaticamente pelo model
        db.session.add(novo_post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('editor.html', form=form, legend="Novo Post", title="Novo Post")

@admin_bp.route('/post/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_post(id):
    """Página para editar um post existente."""
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.conteudo.data
        post.resumo = form.resumo.data
        post.publicado = form.publicado.data
        # Gera um novo slug apenas se o título mudou para evitar quebrar links
        if post.titulo != form.titulo.data:
             post.slug = post.generate_unique_slug(form.titulo.data)
        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('editor.html', form=form, post=post, legend="Editar Post", title="Editar Post")

@admin_bp.route('/post/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_post(id):
    """Ação para deletar um post."""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deletado com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Endpoint para upload de arquivos do CKEditor 5."""
    f = request.files.get('upload')
    if not f:
        return jsonify({'error': {'message': 'Nenhum arquivo enviado.'}}), 400

    filename = secure_filename(f.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
        f.save(filepath)
        url = url_for('static', filename=f'uploads/{filename}', _external=True)
        return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': {'message': f'Erro ao salvar arquivo: {e}'}}), 500