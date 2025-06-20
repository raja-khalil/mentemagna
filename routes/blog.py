# routes/blog.py

from flask import Blueprint, render_template
from models import Post

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/', methods=['GET'])
def blog():
    posts = (
        Post.query
            .filter_by(publicado=True)
            .order_by(Post.data_criacao.desc())
            .all()
    )
    return render_template('blog.html', posts=posts)

@blog_bp.route('/<slug>', methods=['GET'])
def post_detail(slug):
    post = (
        Post.query
            .filter_by(slug=slug, publicado=True)
            .first_or_404()
    )
    
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
                         next_post=next_post)