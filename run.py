import os
from flask import Flask
from config import Config
from extensions import db, migrate, mail, login_manager
from models import User, Post

def create_app(config_class=Config):
    """Cria e configura a instância da aplicação Flask (Application Factory)."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Garante que as pastas de instância e uploads existam
    instance_path = os.path.join(app.instance_path)
    upload_path = app.config['UPLOAD_FOLDER']
    os.makedirs(instance_path, exist_ok=True)
    os.makedirs(upload_path, exist_ok=True)

    # Inicializa as extensões Flask
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Registra os Blueprints
    from routes.main import main_bp
    from routes.blog import blog_bp
    from routes.auth import auth_bp
    from admin.routes import admin_bp
    from routes.solutions import solutions_bp # <-- IMPORTAÇÃO ADICIONADA

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(solutions_bp, url_prefix='/solucoes') # <-- REGISTRO ADICIONADO

    with app.app_context():
        # Cria as tabelas do banco de dados se não existirem
        db.create_all()

        # Cria um usuário admin padrão, se não existir
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('123456') # Mude esta senha em produção!
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário 'admin' criado com senha '123456'.")

    return app

# Cria a aplicação para ser executada
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)