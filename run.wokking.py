import os
from flask import Flask

# Importa as extensões
from extensions import db, migrate, mail, login_manager

# Importa os blueprints
from routes.main import main_bp
from routes.blog import blog_bp
from routes.auth import auth_bp
from admin.routes import admin_bp

def create_app():
    """Cria e configura a aplicação Flask"""
    
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuração direta (sem dotenv)
    app.config['SECRET_KEY'] = 'chave-temporaria-mude-depois'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    
    # Banco SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    
    # Email (configurar depois)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'seu@email.com'
    app.config['MAIL_PASSWORD'] = 'sua-senha'

    # Inicializa extensões (sem CKEditor)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(main_bp)

    return app

# Cria instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Garante criação das tabelas
    with app.app_context():
        db.create_all()
        print('[✅] Banco criado/verificado!')
        
        # Criar usuário admin se não existir
        from models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('123456')
            db.session.add(admin)
            db.session.commit()
            print('[✅] Usuário admin criado - Login: admin / Senha: 123456')
        else:
            print('[ℹ️] Usuário admin já existe')
    
    print('\n🚀 MENTEMAGNA FUNCIONANDO!')
    print('📱 Site: http://localhost:5000')
    print('🔐 Admin: http://localhost:5000/auth/login')
    print('👤 Login: admin / Senha: 123456')
    
    app.run(debug=True, port=5000)