import os
import uuid
from flask import (Blueprint, render_template, redirect, url_for, flash,
                   request, jsonify, current_app)
from flask_login import login_required
from werkzeug.utils import secure_filename
from extensions import db, csrf
from models import Post
from forms import PostForm

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def save_picture(form_picture):
    """Função para salvar a imagem de destaque e retornar o nome do arquivo."""
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    form_picture.save(picture_path)
    # Retorna o caminho relativo a partir da pasta 'static'
    return os.path.join('uploads', picture_fn)

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
        conteudo_editor = request.form.get('conteudo', '')
        novo_post = Post(
            titulo=form.titulo.data,
            conteudo=conteudo_editor,
            resumo=form.resumo.data,
            publicado=form.publicado.data
        )
        if form.imagem.data:
            caminho_imagem = save_picture(form.imagem.data)
            novo_post.imagem = caminho_imagem

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
        post.conteudo = request.form.get('conteudo', '')
        post.titulo = form.titulo.data
        post.resumo = form.resumo.data
        post.publicado = form.publicado.data
        if form.imagem.data:
            caminho_imagem = save_picture(form.imagem.data)
            post.imagem = caminho_imagem
            
        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    # Preenche o campo do formulário com o conteúdo do post para exibição no editor
    form.conteudo.data = post.conteudo
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
@csrf.exempt
@login_required
def upload():
    """Endpoint de upload de arquivos para o CKEditor 5. Mais robusto."""
    f = request.files.get('upload')
    if not f:
        return jsonify({'error': {'message': 'Requisição inválida. Nenhum arquivo no campo "upload".'}}), 400

    try:
        random_hex = uuid.uuid4().hex
        _, f_ext = os.path.splitext(f.filename)
        # Limita as extensões permitidas para maior segurança
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        if f_ext.lower() not in allowed_extensions:
            return jsonify({'error': {'message': 'Tipo de arquivo não permitido.'}}), 400

        filename = secure_filename(random_hex + f_ext)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        f.save(filepath)
        
        url = url_for('static', filename=f'uploads/{filename}', _external=True)
        
        # CKEditor 5 espera uma resposta JSON com a chave 'url'
        return jsonify({'url': url})

    except Exception as e:
        # Loga o erro real no console do Flask para diagnóstico
        current_app.logger.error(f"Erro no upload do CKEditor: {e}")
        return jsonify({'error': {'message': f'Erro interno no servidor ao tentar salvar o arquivo.'}}), 500