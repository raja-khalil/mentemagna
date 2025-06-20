# admin/routes.py - Atualizado para Editor Avançado
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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
@login_required
def dashboard():
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

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Rota para upload de arquivos (imagens e vídeos) - Melhorada"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado', 'success': False}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado', 'success': False}), 400
            
        if file and allowed_file(file.filename):
            # Gerar nome único para evitar conflitos
            import time
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Salvar arquivo
            file.save(filepath)
            
            # URL para acessar o arquivo
            file_url = url_for('static', filename=f'uploads/{filename}')
            
            # Informações do arquivo
            file_size = os.path.getsize(filepath)
            file_type = file.filename.rsplit('.', 1)[1].lower()
            
            return jsonify({
                'success': True,
                'file_url': file_url,
                'filename': filename,
                'original_name': file.filename,
                'file_size': file_size,
                'file_type': file_type,
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
                if f.filename:  # Verifica se um arquivo foi realmente selecionado
                    filename = secure_filename(f.filename)
                    # Adicionar timestamp para evitar conflitos
                    timestamp = str(int(time.time()))
                    filename = f"{timestamp}_{filename}"
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
            
            # Limpar rascunho do localStorage (será feito via JavaScript)
            flash_message = 'Post publicado com sucesso!' if post.publicado else 'Rascunho salvo com sucesso!'
            flash(flash_message, 'success')
            
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar post: {str(e)}', 'danger')
    
    return render_template('editor_advanced.html', form=form, editing=False)

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
                filename = secure_filename(f.filename)
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                f.save(filepath)
                post.imagem = f'/static/uploads/{filename}'
            
            # Regenerar slug se título mudou
            from slugify import slugify
            post.slug = slugify(post.titulo)
            
            db.session.commit()
            
            flash_message = 'Post atualizado com sucesso!' if post.publicado else 'Rascunho atualizado!'
            flash(flash_message, 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar post: {str(e)}', 'danger')
    
    return render_template('editor_advanced.html', form=form, post=post, editing=True)

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

@admin_bp.route('/preview/<int:post_id>')
@login_required
def preview_post(post_id):
    """Preview do post sem publicar"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, preview=True)

@admin_bp.route('/api/auto-save', methods=['POST'])
@login_required
def auto_save():
    """Endpoint para auto-save de rascunhos"""
    try:
        data = request.get_json()
        
        # Aqui você pode implementar auto-save no banco
        # Por enquanto, retorna sucesso para o localStorage
        
        return jsonify({
            'success': True,
            'message': 'Rascunho salvo automaticamente',
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/word-count', methods=['POST'])
@login_required
def word_count():
    """API para contagem de palavras e análise"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        # Análise básica
        words = len(content.split()) if content.strip() else 0
        chars = len(content)
        paragraphs = len([p for p in content.split('\n') if p.strip()])
        
        # Tempo de leitura estimado (200 palavras por minuto)
        reading_time = max(1, round(words / 200))
        
        # SEO score básico
        seo_score = 0
        if words >= 300: seo_score += 25
        if words >= 500: seo_score += 25
        if '<img' in content: seo_score += 25
        if '<a' in content: seo_score += 25
        
        return jsonify({
            'success': True,
            'stats': {
                'words': words,
                'characters': chars,
                'paragraphs': paragraphs,
                'reading_time': reading_time,
                'seo_score': seo_score
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Função auxiliar para limpar HTML
def clean_html(text):
    """Remove tags HTML do texto"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Context processor para injetar funções úteis nos templates
@admin_bp.app_context_processor
def inject_admin_functions():
    return {
        'clean_html': clean_html,
        'datetime': datetime
    }