# routes/blog.py - Rotas Blog Corrigidas

from flask import Blueprint, render_template, abort
from models import Post

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def blog():
    """Página principal do blog"""
    try:
        posts = (
            Post.query
                .filter_by(publicado=True)
                .order_by(Post.data_criacao.desc())
                .all()
        )
        return render_template('blog.html', posts=posts, title="Blog")
    except Exception as e:
        print(f"Erro ao carregar blog: {e}")
        return render_template('blog.html', posts=[], title="Blog")

@blog_bp.route('/<slug>')
def post_detail(slug):
    """Página de detalhes do post"""
    try:
        post = (
            Post.query
                .filter_by(slug=slug, publicado=True)
                .first()
        )
        
        if not post:
            abort(404)
        
        # Incrementar visualizações
        post.views += 1
        from extensions import db
        db.session.commit()
        
        # Buscar posts recentes (últimos 6, excluindo o atual)
        recent_posts = (
            Post.query
                .filter_by(publicado=True)
                .filter(Post.id != post.id)
                .order_by(Post.data_criacao.desc())
                .limit(6)
                .all()
        )
        
        # Buscar post anterior e próximo
        previous_post = (
            Post.query
                .filter_by(publicado=True)
                .filter(Post.data_criacao < post.data_criacao)
                .order_by(Post.data_criacao.desc())
                .first()
        )
        
        next_post = (
            Post.query
                .filter_by(publicado=True)
                .filter(Post.data_criacao > post.data_criacao)
                .order_by(Post.data_criacao.asc())
                .first()
        )
        
        return render_template('post.html', 
                             post=post, 
                             recent_posts=recent_posts,
                             previous_post=previous_post,
                             next_post=next_post,
                             title=post.titulo)
    except Exception as e:
        print(f"Erro ao carregar post: {e}")
        abort(404)