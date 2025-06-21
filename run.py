import os
from flask import Flask
from config import config_by_name
from extensions import db, migrate, mail, login_manager, csrf
from models import User, Post
from routes.solutions import SOLUTIONS_CONFIG
from flask.cli import with_appcontext
import click

def create_app(config_name=None):
    """Cria e configura a instância da aplicação Flask (Application Factory)."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Garante que as pastas de instância e uploads existam
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializa as extensões Flask
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Registra os Blueprints
    from routes.main import main_bp
    from routes.blog import blog_bp
    from routes.auth import auth_bp
    from routes.solutions import solutions_bp
    from routes.sitemap import sitemap_bp
    from admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(solutions_bp, url_prefix='/solucoes')
    app.register_blueprint(sitemap_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context Processor para injetar dados no sidebar
    @app.context_processor
    def inject_sidebar_data():
        """Injeta dados no contexto de todos os templates."""
        try:
            sidebar_posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).limit(5).all()
            sidebar_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active' and v.get('featured', False)}
        except Exception as e:
            app.logger.error(f"Erro ao buscar dados para o sidebar: {e}")
            sidebar_posts = []
            sidebar_solutions = {}
            
        return dict(
            sidebar_posts=sidebar_posts,
            sidebar_solutions=sidebar_solutions
        )

    # Adiciona comandos de linha personalizados
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(set_password_command)

    return app

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Cria as tabelas do banco de dados e um post de exemplo."""
    db.create_all()
    click.echo('Banco de dados inicializado.')
    
    if not Post.query.first():
        post_exemplo = Post(
            titulo="Bem-vindo ao Mente Magna!",
            conteudo="<p>Sua aplicação Flask profissional está no ar. Comece a criar e compartilhar seu conteúdo.</p>",
            resumo="Este é um post de exemplo para demonstrar o blog funcionando.",
            publicado=True
        )
        db.session.add(post_exemplo)
        db.session.commit()
        click.echo('Post de exemplo criado.')

@click.command('create-admin')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_admin_command(username, password):
    """Cria um novo usuário administrador."""
    if User.query.filter_by(username=username).first():
        click.echo(f"Usuário '{username}' já existe.")
        return
    admin_user = User(username=username)
    admin_user.set_password(password)
    db.session.add(admin_user)
    db.session.commit()
    click.echo(f"Usuário administrador '{username}' criado com sucesso.")

@click.command('set-password')
@click.argument('username')
@with_appcontext
def set_password_command(username):
    """Define ou redefine a senha de um usuário de forma interativa."""
    user = User.query.filter_by(username=username).first()
    if user:
        password = click.prompt(f"Digite a nova senha para '{username}'", hide_input=True, confirmation_prompt=True)
        user.set_password(password)
        db.session.commit()
        click.echo(f"A senha para o usuário '{username}' foi redefinida com sucesso.")
    else:
        click.echo(f"Usuário '{username}' não encontrado.")

app = create_app()

if __name__ == '__main__':
    app.run()