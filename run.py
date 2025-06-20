import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, migrate, mail, ckeditor, login_manager
from routes.main import main_bp
from routes.blog import blog_bp
from routes.auth import auth_bp
from admin.routes import admin_bp
from config import config


def create_app():
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()

    # Instancia a aplicação Flask (configurações em instance/)
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Seleciona configuração conforme FLASK_ENV (development, production ou default)
    env = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config.get(env, config['default']))

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)

    # Registra blueprints: autenticação, painel admin, blog e rotas públicas
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(main_bp)

    return app


# Cria instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Garante criação das tabelas se não existirem
    with app.app_context():
        db.create_all()
        print('[✅] Banco criado/verificado em', app.config['SQLALCHEMY_DATABASE_URI'])
    # Executa servidor no modo debug conforme configuração
    app.run(debug=app.config.get('DEBUG', False))
