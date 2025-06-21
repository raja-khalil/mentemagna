from flask import Blueprint, render_template, abort
from models import Post

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def blog():
    """Exibe a lista de posts publicados."""
    posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).all()
    return render_template('blog.html', posts=posts, title="Blog")

@blog_bp.route('/<string:slug>')
def post(slug):
    """Exibe um post individual."""
    post = Post.query.filter_by(slug=slug, publicado=True).first_or_404()
    post.views += 1
    from extensions import db
    db.session.commit()
    return render_template('post.html', post=post, title=post.titulo)