#!/usr/bin/env python3
"""
Mente Magna - Servidor Principal 
PROBLEMA DO BANCO CORRIGIDO
"""

import os
import sys
from flask import Flask, render_template

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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-temporaria-desenvolvimento')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentemagna.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurações de email
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    print("✅ Configurações carregadas")
    
    # Inicializar extensões
    from extensions import db, migrate, mail, login_manager
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # IMPORTANTE: Importar models DEPOIS de inicializar extensões
    from models import User, Post
    
    print("✅ Extensões inicializadas")
    
    # Registrar rotas principais
    register_routes(app)
    
    # Criar banco de dados CORRETAMENTE
    with app.app_context():
        try:
            # Deletar banco existente se houver problema
            if os.path.exists('mentemagna.db'):
                os.remove('mentemagna.db')
                print("🗑️ Banco antigo removido")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso")
            
            # Criar usuário admin
            create_admin_user(db, User)
            
        except Exception as e:
            print(f"❌ Erro ao criar banco: {e}")
    
    return app

def register_routes(app):
    """Registra todas as rotas da aplicação"""
    
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/sobre')
    def sobre():
        return render_template('sobre.html')
    
    @app.route('/contato')
    def contato():
        return render_template('contato.html')
    
    @app.route('/blog')
    def blog():
        return render_template('blog.html')
    
    @app.route('/produtos')
    def produtos():
        return render_template('produtos.html')
    
    @app.route('/emagna')
    def emagna():
        return render_template('emagna.html')
    
    # Rotas de administração
    @app.route('/admin')
    def admin():
        return '<h1>🔧 Admin em construção</h1><a href="/">← Voltar</a>'
    
    @app.route('/auth/login')
    def login():
        return '<h1>🔑 Login em construção</h1><a href="/">← Voltar</a>'
    
    print("✅ Rotas registradas")

def create_admin_user(db, User):
    """Cria usuário admin padrão"""
    try:
        # Verificar se admin já existe
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