# admin/routes.py - Rotas Admin Corrigidas
import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from extensions import db
from models import Post
from forms import PostForm

admin_bp = Blueprint('admin', __name__, template_folder='templates')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
@login_required
def dashboard():
    try:
        posts = Post.query.order_by(Post.data_criacao.desc()).all()
        
        # Estatísticas para o dashboard
        stats = {
            'total_posts': len(posts),
            'published_posts': len([p for p in posts if p.publicado]),
            'draft_posts': len([p for p in posts if not p.publicado]),
            'total_views': sum(p.views for p in posts),
            'this_week_posts': len([p for p in posts if (datetime.now() - p.data_criacao).days <= 7])
        }
        
        return render_template('dashboard.html', posts=posts, stats=stats)
    except Exception as e:
        flash(f'Erro ao carregar dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', posts=[], stats={
            'total_posts': 0, 'published_posts': 0, 'draft_posts': 0, 
            'total_views': 0, 'this_week_posts': 0
        })

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Rota para upload de arquivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado', 'success': False}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado', 'success': False}), 400
            
        if file and allowed_file(file.filename):
            # Gerar nome único
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Salvar arquivo
            file.save(filepath)
            
            # URL para acessar o arquivo
            file_url = url_for('static', filename=f'uploads/{filename}')
            
            return jsonify({
                'success': True,
                'file_url': file_url,
                'filename': filename,
                'message': 'Upload realizado com sucesso!'
            })
        else:
            return jsonify({
                'error': f'Tipo de arquivo não permitido. Use: {", ".join(ALLOWED_EXTENSIONS)}',
                'success': False
            }), 400
            
    except Exception as e:
        return jsonify({
            'error': f'Erro no upload: {str(e)}',
            'success': False
        }), 500

@admin_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            # Upload de imagem principal (se houver)
            filename = None
            if form.imagem.data:
                f = form.imagem.data
                if f.filename and allowed_file(f.filename):
                    timestamp = str(int(time.time()))
                    filename = f"{timestamp}_{secure_filename(f.filename)}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    f.save(filepath)
            
            # Criar o post
            post = Post(
                titulo=form.titulo.data,
                conteudo=form.conteudo.data,
                resumo=form.resumo.data,
                imagem=f'/static/uploads/{filename}' if filename else None,
                publicado=form.publicado.data
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash_message = 'Post publicado com sucesso!' if post.publicado else 'Rascunho salvo com sucesso!'
            flash(flash_message, 'success')
            
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar post: {str(e)}', 'error')
    
    return render_template('editor.html', form=form, legend="Novo Post")

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
            post.resumo = form.resumo.data
            post.publicado = form.publicado.data
            post.data_atualizacao = datetime.utcnow()
            
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
                if allowed_file(f.filename):
                    timestamp = str(int(time.time()))
                    filename = f"{timestamp}_{secure_filename(f.filename)}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    f.save(filepath)
                    post.imagem = f'/static/uploads/{filename}'
            
            # Regenerar slug se título mudou
            post.slug = post.generate_slug()
            
            db.session.commit()
            
            flash_message = 'Post atualizado com sucesso!' if post.publicado else 'Rascunho atualizado!'
            flash(flash_message, 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar post: {str(e)}', 'error')
    
    return render_template('editor.html', form=form, post=post, legend="Editar Post")

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
        flash(f'Erro ao deletar post: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))