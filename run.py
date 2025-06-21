#!/usr/bin/env python3
"""
Mente Magna - Versão que Funciona
"""

import os
import sys
from pathlib import Path

# Carregar .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask

def create_app():
    """Cria aplicação Flask funcional"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = 'mente-magna-secret-key-2025'
    
    # SQLite com caminho absoluto para evitar problemas
    base_dir = Path(__file__).parent.absolute()
    instance_dir = base_dir / 'instance'
    db_file = instance_dir / 'database.db'
    
    # Garantir que o diretório existe
    instance_dir.mkdir(exist_ok=True)
    
    # URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email (opcional)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    # Upload
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = str(base_dir / 'static' / 'uploads')
    
    # Inicializar extensões
    from extensions import db, migrate, mail, login_manager
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # Registrar blueprints
    try:
        from routes.main import main_bp
        from routes.blog import blog_bp
        from routes.auth import auth_bp
        from admin.routes import admin_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(blog_bp, url_prefix='/blog')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        print("Blueprints registrados com sucesso")
    except ImportError as e:
        print(f"Erro ao importar blueprints: {e}")
        # Continuar mesmo com erro de blueprint
    
    # Inicializar banco de dados
    with app.app_context():
        try:
            from models import User, Post
            
            # Criar tabelas
            db.create_all()
            print("Banco de dados criado com sucesso")
            
            # Criar usuário admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', email='admin@mentemagna.com')
                admin.set_password('123456')
                db.session.add(admin)
                db.session.commit()
                print("Usuário admin criado: admin/123456")
            
            # Criar post de exemplo
            if Post.query.count() == 0:
                post = Post(
                    titulo="Bem-vindo ao Mente Magna!",
                    conteudo="<h1>Sistema funcionando!</h1><p>Sua aplicação está rodando sem erros.</p>",
                    resumo="Post de boas-vindas do Mente Magna",
                    publicado=True
                )
                db.session.add(post)
                db.session.commit()
                print("Post de exemplo criado")
                
        except Exception as e:
            print(f"Erro na inicialização do banco: {e}")
            # Criar banco vazio se houver erro
            try:
                db.create_all()
                print("Banco básico criado")
            except:
                print("Não foi possível criar o banco")
    
    return app

def main():
    """Função principal"""
    # Garantir diretórios
    base_dir = Path(__file__).parent.absolute()
    
    # Criar diretórios essenciais
    (base_dir / 'static' / 'uploads').mkdir(parents=True, exist_ok=True)
    (base_dir / 'instance').mkdir(exist_ok=True)
    
    print("MENTE MAGNA - INICIANDO...")
    print("=" * 40)
    
    # Criar app
    app = create_app()
    
    print("SERVIDOR FUNCIONANDO!")
    print("URL: http://localhost:5000")
    print("Admin: http://localhost:5000/auth/login")
    print("Login: admin / 123456")
    print("=" * 40)
    
    # Executar servidor
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Servidor finalizado")

if __name__ == '__main__':
    main()
