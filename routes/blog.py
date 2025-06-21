from flask import Blueprint, render_template, abort
from models import Post
from extensions import db
from routes.solutions import SOLUTIONS_CONFIG

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def blog():
    """Exibe a lista de posts publicados."""
    posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).all()
    return render_template('blog.html', posts=posts, title="Blog")

@blog_bp.route('/<string:slug>')
def post_detail(slug):
    """Exibe um post individual e conteúdo para a sidebar."""
    post = Post.query.filter_by(slug=slug, publicado=True).first_or_404()
    
    # Atualiza visualizações
    post.views = (post.views or 0) + 1
    db.session.commit()
    
    # Busca posts recentes para a sidebar (excluindo o atual)
    recent_posts = Post.query.filter(Post.id != post.id, Post.publicado==True).order_by(Post.data_criacao.desc()).limit(5).all()
    
    # Pega as soluções ativas para a sidebar
    active_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active'}
    
    return render_template(
        'post.html', 
        post=post, 
        title=post.titulo, 
        description=post.resumo,
        recent_posts=recent_posts,
        solutions=active_solutions
    )