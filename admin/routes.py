# admin/routes.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from extensions import db
from models import Post
from forms import PostForm

admin_bp = Blueprint('admin', __name__, template_folder='templates')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','mp4'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
@login_required
def dashboard():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('dashboard.html', posts=posts)

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Rota para upload de arquivos (imagens e vídeos)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
        if file and allowed_file(file.filename):
            # Gerar nome único para evitar conflitos
            import time
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            file_url = url_for('static', filename=f'uploads/{filename}')
            return jsonify({
                'success': True,
                'file_url': file_url,
                'filename': filename
            })
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido. Use: PNG, JPG, JPEG, GIF, MP4'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@admin_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            # Upload de imagem (se houver)
            filename = None
            if form.imagem.data:
                f = form.imagem.data
                if f.filename:  # Verifica se um arquivo foi realmente selecionado
                    filename = secure_filename(f.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    f.save(filepath)
            
            # Criar o post
            post = Post(
                titulo=form.titulo.data,
                conteudo=form.conteudo.data,
                imagem=f'/static/uploads/{filename}' if filename else None,
                publicado=form.publicado.data,
                data_criacao=datetime.utcnow()
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash(f'Post "{post.titulo}" publicado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar post: {str(e)}', 'danger')
    
    return render_template('editor.html', form=form, editing=False)

@admin_bp.route('/editar/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        try:
            # Atualizar campos do post
            post.titulo = form.titulo.data
            post.conteudo = form.conteudo.data
            post.publicado = form.publicado.data
            
            # Upload de nova imagem (se houver)
            if form.imagem.data and form.imagem.data.filename:
                # Remover imagem antiga
                if post.imagem:
                    old_path = post.imagem.replace('/static/', 'static/')
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except:
                            pass
                
                # Salvar nova imagem
                f = form.imagem.data
                filename = secure_filename(f.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                f.save(filepath)
                post.imagem = f'/static/uploads/{filename}'
            
            # Regenerar slug se título mudou
            from slugify import slugify
            post.slug = slugify(post.titulo)
            
            db.session.commit()
            flash(f'Post "{post.titulo}" atualizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar post: {str(e)}', 'danger')
    
    return render_template('editor.html', form=form, post=post, editing=True)

@admin_bp.route('/deletar/<int:post_id>', methods=['POST'])
@login_required
def deletar_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        titulo = post.titulo
        
        # Remover arquivo de imagem se existir
        if post.imagem:
            try:
                file_path = post.imagem.replace('/static/', 'static/')
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
        
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{titulo}" deletado com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar post: {str(e)}', 'danger')
    
    return redirect(url_for('admin.dashboard'))