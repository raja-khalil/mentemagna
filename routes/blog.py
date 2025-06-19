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
    return render_template('post.html', post=post)
