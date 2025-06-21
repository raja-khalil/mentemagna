#!/usr/bin/env python3
"""
Mente Magna - Servidor Principal Simplificado
"""

import os
import sys
from flask import Flask

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Arquivo .env carregado")
except ImportError:
    print("⚠️ python-dotenv não encontrado")

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentemagna.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurações de email
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    # Configurações de upload
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    
    print("✅ Configurações carregadas")
    
    # Inicializar extensões
    from extensions import db, migrate, mail, login_manager
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    print("✅ Extensões inicializadas")
    
    # Importar modelos APÓS inicializar extensões
    from models import User, Post
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Criar banco de dados
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados criado/verificado")
            
            # Criar usuário admin se não existir
            create_admin_user(db, User)
            
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
    
    return app

def register_blueprints(app):
    """Registra todos os blueprints"""
    
    # Rotas principais
    from routes.main import main_bp
    from routes.blog import blog_bp
    from routes.auth import auth_bp
    
    # Blueprint admin
    from admin.routes import admin_bp
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    print("✅ Blueprints registrados")

def create_admin_user(db, User):
    """Cria usuário admin padrão"""
    try:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@mentemagna.com'
            )
            admin.set_password('123456')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado (admin/123456)")
        else:
            print("ℹ️ Usuário admin já existe")
            
    except Exception as e:
        print(f"⚠️ Erro ao criar admin: {e}")

def show_startup_info():
    """Mostra informações de inicialização"""
    print("\n" + "=" * 60)
    print("🚀 MENTE MAGNA - SERVIDOR FUNCIONANDO!")
    print("=" * 60)
    print("\n🌐 ACESSE:")
    print("📱 Site: http://localhost:5000")
    print("📄 Sobre: http://localhost:5000/sobre")
    print("📝 Blog: http://localhost:5000/blog")
    print("📞 Contato: http://localhost:5000/contato")
    
    print("\n👤 ADMIN:")
    print("   URL: http://localhost:5000/auth/login")
    print("   Usuário: admin")
    print("   Senha: 123456")
    
    print("\n📧 EMAIL CONFIGURADO:")
    print(f"   {os.getenv('MAIL_USERNAME', 'Não configurado')}")
    
    print("\n⏹️ Para parar: Ctrl+C")
    print("=" * 60)

if __name__ == '__main__':
    app = create_app()
    show_startup_info()
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor finalizado")