# routes/blog.py
from flask import Blueprint, render_template
from models import Post

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('blog.html', title="Blog", posts=posts)

@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)
