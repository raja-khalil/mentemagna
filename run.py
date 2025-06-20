import os
from flask import Flask

# Tentar importar dotenv, mas funcionar mesmo sem ele
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv não encontrado, usando configurações padrão")

from extensions import db, migrate, mail, login_manager
from routes.main import main_bp
from routes.blog import blog_bp
from routes.auth import auth_bp
from routes.sitemap import sitemap_bp

# NOVA IMPORTAÇÃO: Sistema de soluções
try:
    from routes.solutions import solutions_bp
    SOLUTIONS_AVAILABLE = True
except ImportError:
    print("⚠️ Sistema de soluções não encontrado. Execute: python run_setup.py")
    SOLUTIONS_AVAILABLE = False

from admin.routes import admin_bp
from config import config


def create_app():
    # Instancia a aplicação Flask (configurações em instance/)
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Seleciona configuração conforme FLASK_ENV (development, production ou default)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config.get(env, config['development']))

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Registra blueprints: autenticação, painel admin, blog, sitemap e rotas públicas
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(sitemap_bp)  # Sem prefixo para sitemap.xml na raiz
    
    # NOVO: Registrar blueprint de soluções
    if SOLUTIONS_AVAILABLE:
        app.register_blueprint(solutions_bp)
        print("✅ Sistema de soluções carregado!")
    
    app.register_blueprint(main_bp)

    return app


# Cria instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Garante criação das tabelas se não existirem
    with app.app_context():
        db.create_all()
        print('[✅] Banco criado/verificado em', app.config['SQLALCHEMY_DATABASE_URI'])
        
        # Criar usuário admin padrão se não existir
        from models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('123456')  # Senha temporária
            db.session.add(admin)
            db.session.commit()
            print('[✅] Usuário admin criado - Login: admin / Senha: 123456')
        else:
            print('[ℹ️] Usuário admin já existe')
        
        # Criar categorias padrão se sistema de soluções estiver disponível
        if SOLUTIONS_AVAILABLE:
            try:
                from models import Category
                categories_count = Category.query.count()
                if categories_count == 0:
                    # Criar categorias básicas
                    default_categories = [
                        {'name': 'Inteligência Artificial', 'icon': '🤖', 'color': '#e74c3c'},
                        {'name': 'Programação', 'icon': '💻', 'color': '#3498db'},
                        {'name': 'Web Development', 'icon': '🌐', 'color': '#2ecc71'},
                        {'name': 'Ferramentas', 'icon': '🔧', 'color': '#f39c12'},
                    ]
                    
                    for cat_data in default_categories:
                        category = Category(**cat_data)
                        db.session.add(category)
                    
                    db.session.commit()
                    print('[✅] Categorias padrão criadas')
                
            except Exception as e:
                print(f'[⚠️] Erro ao criar categorias: {e}')
    
    # URLs importantes do sistema
    print('\n🚀 MENTEMAGNA FUNCIONANDO!')
    print('📱 Site: http://localhost:5000')
    print('🔐 Admin: http://localhost:5000/auth/login')
    print('👤 Login: admin / Senha: 123456')
    print('📝 Blog: http://localhost:5000/blog')
    
    if SOLUTIONS_AVAILABLE:
        print('🔧 Soluções: http://localhost:5000/solucoes')
        print('🏥 CID: http://localhost:5000/solucoes/consulta-cid')
        print('👔 CBO: http://localhost:5000/solucoes/consulta-cbo')
    
    print('🗺️ Sitemap: http://localhost:5000/sitemap.xml')
    print('🤖 Robots: http://localhost:5000/robots.txt')
    print('\nPressione Ctrl+C para parar')
    
    app.run(debug=app.config.get('DEBUG', True))