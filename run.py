#!/usr/bin/env python3
"""
Mente Magna - Servidor Principal com Sistema de Backup
"""

import os
import sys
from flask import Flask

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Tentar importar dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Arquivo .env carregado")
except ImportError:
    print("⚠️ python-dotenv não encontrado, usando configurações padrão")
except FileNotFoundError:
    print("⚠️ Arquivo .env não encontrado, usando configurações padrão")

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Criar pasta instance se não existir
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Carregar configurações
    env = os.getenv('FLASK_ENV', 'development')
    from config import config
    app.config.from_object(config.get(env, config['development']))
    
    print(f"✅ Ambiente: {env}")
    print(f"📁 Pasta instance: {app.instance_path}")
    print(f"🗄️ Banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Inicializar extensões
    try:
        from extensions import db, migrate, mail, login_manager
        
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)
        login_manager.init_app(app)
        
        print("✅ Extensões inicializadas")
        
    except ImportError as e:
        print(f"❌ Erro ao importar extensões: {e}")
        return None
    
    # Registrar blueprints
    try:
        # Blueprints básicos
        from routes.main import main_bp
        app.register_blueprint(main_bp)
        print("✅ Blueprint main registrado")
        
        # Blueprints opcionais
        blueprints = [
            ('routes.blog', 'blog_bp', '/blog'),
            ('routes.auth', 'auth_bp', '/auth'),
            ('admin.routes', 'admin_bp', '/admin'),
            ('routes.sitemap', 'sitemap_bp', None),
            ('routes.solutions', 'solutions_bp', None)
        ]
        
        for module_name, blueprint_name, url_prefix in blueprints:
            try:
                module = __import__(module_name, fromlist=[blueprint_name])
                blueprint = getattr(module, blueprint_name)
                if url_prefix:
                    app.register_blueprint(blueprint, url_prefix=url_prefix)
                else:
                    app.register_blueprint(blueprint)
                print(f"✅ Blueprint {blueprint_name} registrado")
            except ImportError:
                print(f"⚠️ Blueprint {blueprint_name} não encontrado")
            except Exception as e:
                print(f"⚠️ Erro ao registrar {blueprint_name}: {e}")
                
    except ImportError as e:
        print(f"❌ Erro ao registrar blueprints: {e}")
        return None
    
    return app

def initialize_database_with_backup(app):
    """Inicializa o banco de dados com sistema de backup"""
    try:
        # Importar o gerenciador de backup
        from database_manager import setup_database_with_backup
        
        # Configurar banco com backup automático
        db_manager = setup_database_with_backup(app)
        
        # Criar backup automático a cada inicialização
        backup_path = db_manager.create_backup(f"startup_{os.getenv('FLASK_ENV', 'dev')}.db")
        print(f"🔒 Backup automático criado: {backup_path}")
        
        # Limpeza automática de backups antigos (manter últimos 20)
        db_manager.cleanup_old_backups(keep_count=20)
        
        return db_manager
        
    except ImportError:
        print("⚠️ Sistema de backup não encontrado, usando inicialização padrão")
        
        # Fallback para inicialização padrão
        with app.app_context():
            from extensions import db
            from models import User, Post
            
            db.create_all()
            print("✅ Banco de dados inicializado (sem backup)")
            
            # Criar usuário admin se não existir
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin')
                admin.set_password('123456')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado (admin/123456)")
            
            # Estatísticas
            total_posts = Post.query.count()
            total_users = User.query.count()
            print(f"📊 Posts: {total_posts} | Usuários: {total_users}")
            
        return None

def show_startup_info(app, db_manager=None):
    """Mostra informações de inicialização"""
    print("\n" + "=" * 60)
    print("🚀 MENTE MAGNA - SERVIDOR INICIADO COM SUCESSO!")
    print("=" * 60)
    
    # URLs do sistema
    print("\n🌐 URLS DISPONÍVEIS:")
    print("📱 Site Principal: http://localhost:5000")
    print("🔐 Painel Admin: http://localhost:5000/auth/login")
    print("📝 Blog: http://localhost:5000/blog")
    print("🔧 Soluções: http://localhost:5000/solucoes")
    print("🗺️ Sitemap: http://localhost:5000/sitemap.xml")
    print("🤖 Robots: http://localhost:5000/robots.txt")
    
    # Credenciais
    print("\n👤 CREDENCIAIS PADRÃO:")
    print("   Usuário: admin")
    print("   Senha: 123456")
    print("   ⚠️ MUDE A SENHA EM PRODUÇÃO!")
    
    # Informações do banco
    print(f"\n🗄️ BANCO DE DADOS:")
    print(f"   Tipo: {app.config['SQLALCHEMY_DATABASE_URI'].split(':')[0].upper()}")
    print(f"   Local: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Informações de backup
    if db_manager:
        backups = db_manager.list_backups()
        print(f"   📦 Backups: {len(backups)} disponíveis")
        if backups:
            print(f"   📅 Último: {backups[0]['filename']}")
    
    # Comandos úteis
    print("\n⚙️ COMANDOS ÚTEIS:")
    print("   python database_manager.py backup    - Criar backup manual")
    print("   python database_manager.py list      - Listar backups")
    print("   python database_manager.py export    - Exportar dados")
    
    # Status de produção
    if app.config.get('DEBUG'):
        print("\n🔧 MODO: Desenvolvimento (DEBUG ativo)")
    else:
        print("\n🏭 MODO: Produção")
        print("   ⚠️ Certifique-se de que as configurações estão corretas!")
    
    print("\n⏹️ Para parar o servidor: Ctrl+C")
    print("=" * 60)

def main():
    """Função principal"""
    print("🚀 INICIANDO MENTE MAGNA COM SISTEMA DE BACKUP")
    print("=" * 60)
    
    # Criar aplicação
    app = create_app()
    if not app:
        print("❌ Falha ao criar aplicação")
        sys.exit(1)
    
    # Inicializar banco com backup
    db_manager = initialize_database_with_backup(app)
    
    # Mostrar informações de inicialização
    show_startup_info(app, db_manager)
    
    # Iniciar servidor
    try:
        app.run(
            debug=app.config.get('DEBUG', True),
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Desabilita reloader para evitar backups duplicados
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor finalizado pelo usuário")
        
        # Criar backup final ao sair
        if db_manager:
            final_backup = db_manager.create_backup("shutdown_backup.db")
            print(f"🔒 Backup final criado: {final_backup}")
            
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")

if __name__ == '__main__':
    main()