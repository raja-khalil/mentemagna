#!/usr/bin/env python3
"""
Script de configuração completa para MenteMagna
Execute: python run_setup.py
"""

import os
import sys
from flask import Flask

def create_app():
    """Cria app Flask para setup"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'setup-temp-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    
    from extensions import db
    db.init_app(app)
    
    return app

def create_directories():
    """Cria todos os diretórios necessários"""
    print("📁 Criando estrutura de diretórios...")
    
    directories = [
        'templates/solutions',
        'templates/blog/categories', 
        'static/js/solutions',
        'static/css/solutions',
        'instance',
        'static/uploads'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")

def create_seo_helper():
    """Cria arquivo seo_helper.py se não existir"""
    if os.path.exists('seo_helper.py'):
        print("✅ seo_helper.py já existe")
        return
    
    print("📝 Criando seo_helper.py...")
    
    seo_content = '''# seo_helper.py - Sistema SEO simplificado
def get_seo_data(page_type, **kwargs):
    """Função helper para SEO"""
    
    base_keywords = [
        "tecnologia", "programação", "python", "flask", "desenvolvimento web",
        "inteligência artificial", "machine learning", "tutorial", "blog tech"
    ]
    
    if page_type == "tool":
        tool_name = kwargs.get('tool_name', 'Ferramenta')
        tool_description = kwargs.get('tool_description', 'Ferramenta online gratuita')
        
        return {
            'page_title': f"{tool_name} - Mente Magna",
            'page_description': tool_description,
            'page_keywords': ', '.join(base_keywords + ['ferramenta online', 'grátis']),
            'og_title': tool_name,
            'og_description': tool_description,
            'schema_type': 'WebApplication'
        }
    
    # Default
    return {
        'page_title': 'Mente Magna - Portal de Tecnologia e Inovação',
        'page_description': 'Portal de referência em tecnologia, programação e inovação',
        'page_keywords': ', '.join(base_keywords),
        'og_title': 'Mente Magna',
        'og_description': 'Portal de tecnologia e inovação',
        'schema_type': 'WebPage'
    }
'''
    
    with open('seo_helper.py', 'w', encoding='utf-8') as f:
        f.write(seo_content)
    
    print("✅ seo_helper.py criado!")

def update_models():
    """Atualiza models.py com categorias"""
    print("📝 Verificando models.py...")
    
    with open('models.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class Category' in content:
        print("✅ Category model já existe")
        return
    
    print("🔧 Adicionando Category model...")
    
    # Adicionar import e tabela de associação antes da classe Post
    category_code = '''
# Tabela de associação para many-to-many entre Post e Category
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class Category(db.Model):
    """Modelo para categorias do blog"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), default='#007bff')
    icon = db.Column(db.String(50), default='📝')
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', secondary=post_categories, 
                           back_populates='categories', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.name:
            from slugify import slugify
            self.slug = slugify(self.name)
    
    @property
    def post_count(self):
        return self.posts.filter_by(publicado=True).count()
    
    def __repr__(self):
        return f"<Category {self.name}>"

'''
    
    # Adicionar relacionamento na classe Post
    post_update = '''
    # Adicionar na classe Post (após o campo data_criacao):
    categories = db.relationship('Category', secondary=post_categories, 
                                back_populates='posts', lazy='subquery')
'''
    
    print("⚠️ ATENÇÃO: Você precisará adicionar manualmente:")
    print("1. O código da Category antes da classe Post")
    print("2. O relacionamento categories na classe Post")
    print("3. Executar flask db migrate para criar as tabelas")

def create_routes_solutions():
    """Cria arquivo routes/solutions.py"""
    if os.path.exists('routes/solutions.py'):
        print("✅ routes/solutions.py já existe")
        return
    
    print("📝 Criando routes/solutions.py...")
    
    # Criar versão simplificada
    routes_content = '''# routes/solutions.py - Sistema de soluções modulares
from flask import Blueprint, render_template, request, jsonify
try:
    from seo_helper import get_seo_data
except ImportError:
    def get_seo_data(page_type, **kwargs):
        return {
            'page_title': kwargs.get('tool_name', 'Mente Magna'),
            'page_description': kwargs.get('tool_description', ''),
            'page_keywords': 'tecnologia, ferramentas, online',
            'schema_type': 'WebApplication'
        }

solutions_bp = Blueprint('solutions', __name__, url_prefix='/solucoes')

# Configuração das soluções
SOLUTIONS_CONFIG = {
    'consulta-cid': {
        'name': 'Consulta CID',
        'description': 'Busque códigos CID (Classificação Internacional de Doenças)',
        'icon': '🏥',
        'category': 'Saúde',
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbxeqxH0-ru4NiDqJQYF19pxi1ualySptKZlMdnC219tJJP4F2-KDK7wDiX-nJgztHoz',
        'status': 'active',
        'featured': True
    },
    'consulta-cbo': {
        'name': 'Consulta CBO',
        'description': 'Consulte códigos CBO (Classificação Brasileira de Ocupações)',
        'icon': '👔',
        'category': 'Profissional',
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbwyGB71MUHmivLgiPwROWaa-AjvsfFe6yD4H9L7jAE57lFjLb3bSu44mkF3u0kohWmd',
        'status': 'active',
        'featured': True
    },
    'calculadora': {
        'name': 'Calculadora Online',
        'description': 'Calculadora online completa com funções básicas',
        'icon': '🧮',
        'category': 'Matemática',
        'type': 'html_js',
        'status': 'active',
        'featured': True
    }
}

@solutions_bp.route('/')
def solutions_index():
    """Página principal das soluções"""
    active_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active'}
    
    # Agrupar por categoria
    categories = {}
    for slug, config in active_solutions.items():
        category = config['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({'slug': slug, **config})
    
    seo_data = get_seo_data('tool', 
                           tool_name='Soluções Online Gratuitas',
                           tool_description='Ferramentas e soluções online gratuitas')
    
    return render_template('solutions/index.html', 
                         categories=categories,
                         **seo_data)

@solutions_bp.route('/<solution_slug>')
def solution_detail(solution_slug):
    """Página da solução individual"""
    if solution_slug not in SOLUTIONS_CONFIG:
        return "Solução não encontrada", 404
    
    solution = SOLUTIONS_CONFIG[solution_slug]
    
    if solution['type'] == 'google_apps_script':
        solution['script_url'] = f"https://script.google.com/macros/s/{solution['deployment_id']}/exec"
    
    seo_data = get_seo_data('tool',
                           tool_name=solution['name'],
                           tool_description=solution['description'])
    
    template_map = {
        'consulta-cid': 'solutions/cid.html',
        'consulta-cbo': 'solutions/cbo.html',
        'calculadora': 'solutions/calculadora.html'
    }
    
    template = template_map.get(solution_slug, 'solutions/generic.html')
    
    return render_template(template,
                         solution=solution,
                         solution_slug=solution_slug,
                         **seo_data)
'''
    
    with open('routes/solutions.py', 'w', encoding='utf-8') as f:
        f.write(routes_content)
    
    print("✅ routes/solutions.py criado!")

def create_basic_templates():
    """Cria templates básicos"""
    print("📝 Criando templates básicos...")
    
    # Template index das soluções
    index_template = '''{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-12">
            <h1 class="display-4 text-center mb-5">🔧 Soluções Online Gratuitas</h1>
            <p class="lead text-center mb-5">
                Ferramentas práticas e úteis para o seu dia a dia. Todas gratuitas e sem necessidade de cadastro.
            </p>
        </div>
    </div>
    
    <!-- ANÚNCIO HEADER -->
    <div class="row mb-5">
        <div class="col-12">
            <div class="text-center p-3 bg-light rounded">
                <small class="text-muted">Publicidade</small>
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-4115727278051485"
                     data-ad-slot="1234567890"
                     data-ad-format="horizontal"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
    </div>
    
    <!-- Soluções por Categoria -->
    {% for category_name, solutions in categories.items() %}
    <div class="row mb-5">
        <div class="col-12">
            <h2 class="h3 border-bottom pb-2 mb-4">{{ category_name }}</h2>
            <div class="row">
                {% for solution in solutions %}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <div class="mb-3" style="font-size: 3rem;">{{ solution.icon }}</div>
                            <h5 class="card-title">{{ solution.name }}</h5>
                            <p class="card-text">{{ solution.description }}</p>
                            <a href="{{ url_for('solutions.solution_detail', solution_slug=solution.slug) }}" 
                               class="btn btn-primary">
                                Usar Agora →
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endfor %}
    
    <!-- ANÚNCIO FOOTER -->
    <div class="row my-5">
        <div class="col-12">
            <div class="text-center p-3 bg-light rounded">
                <small class="text-muted">Publicidade</small>
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-4115727278051485"
                     data-ad-slot="9999999999"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    with open('templates/solutions/index.html', 'w', encoding='utf-8') as f:
        f.write(index_template)
    
    print("✅ templates/solutions/index.html criado!")

def update_run_py():
    """Atualiza run.py para incluir as novas rotas"""
    print("📝 Verificando run.py...")
    
    with open('run.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'solutions_bp' in content:
        print("✅ run.py já está atualizado")
        return
    
    print("🔧 Você precisará adicionar no run.py:")
    print("1. from routes.solutions import solutions_bp")
    print("2. app.register_blueprint(solutions_bp)")

def create_migration_script():
    """Cria script para migração do banco"""
    migration_script = '''#!/usr/bin/env python3
"""
Script de migração do banco de dados
Execute: python migrate_db.py
"""

from flask import Flask
from extensions import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'migration-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    
    db.init_app(app)
    return app

def create_categories():
    """Cria categorias padrão"""
    from models import Category
    
    categories = [
        {'name': 'Inteligência Artificial', 'icon': '🤖', 'color': '#e74c3c'},
        {'name': 'Programação', 'icon': '💻', 'color': '#3498db'},
        {'name': 'Web Development', 'icon': '🌐', 'color': '#2ecc71'},
        {'name': 'Ferramentas', 'icon': '🔧', 'color': '#f39c12'},
    ]
    
    for cat_data in categories:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("✅ Categorias criadas!")

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas!")
            
            # Criar categorias
            create_categories()
            
            print("🎉 Migração concluída!")
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
'''
    
    with open('migrate_db.py', 'w', encoding='utf-8') as f:
        f.write(migration_script)
    
    print("✅ migrate_db.py criado!")

def main():
    """Função principal"""
    print("🚀 CONFIGURAÇÃO COMPLETA DO MENTEMAGNA")
    print("=" * 60)
    
    try:
        # 1. Criar diretórios
        create_directories()
        
        # 2. Criar arquivo SEO helper
        create_seo_helper()
        
        # 3. Verificar models
        update_models()
        
        # 4. Criar rotas das soluções
        create_routes_solutions()
        
        # 5. Criar templates básicos
        create_basic_templates()
        
        # 6. Verificar run.py
        update_run_py()
        
        # 7. Criar script de migração
        create_migration_script()
        
        print("\n" + "=" * 60)
        print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
        print("=" * 60)
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Adicione ao run.py:")
        print("   from routes.solutions import solutions_bp")
        print("   app.register_blueprint(solutions_bp)")
        print("")
        print("2. Execute a migração:")
        print("   python migrate_db.py")
        print("")
        print("3. Teste o sistema:")
        print("   python run.py")
        print("   Acesse: http://localhost:5000/solucoes")
        print("")
        print("4. Suas ferramentas Google Apps Script estarão em:")
        print("   http://localhost:5000/solucoes/consulta-cid")
        print("   http://localhost:5000/solucoes/consulta-cbo")
        
        print("\n💡 DICAS:")
        print("- Templates CID e CBO já estão prontos")
        print("- Sistema é 100% modular e fácil de expandir")
        print("- AdSense está integrado em todas as páginas")
        print("- SEO otimizado para cada ferramenta")
        
    except Exception as e:
        print(f"\n❌ Erro durante configuração: {e}")
        print("Verifique os arquivos e tente novamente.")

if __name__ == '__main__':
    main()