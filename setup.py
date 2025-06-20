#!/usr/bin/env python3
"""
Script de inicialização do projeto Mente Magna
Execute este arquivo para configurar tudo automaticamente
"""

import os
import sys

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    if sys.version_info < (3, 8):
        print("❌ ERRO: Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        'instance',
        'static/uploads',
        'static/img',
        'static/css',
        'static/js',
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Diretório criado: {directory}")
        else:
            print(f"ℹ️ Diretório já existe: {directory}")

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        env_content = '''# Configurações do Mente Magna
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu@email.com
MAIL_PASSWORD=sua-senha-de-app
'''
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
        print("⚠️ IMPORTANTE: Edite o arquivo .env com suas configurações!")
    else:
        print("ℹ️ Arquivo .env já existe")

def install_requirements():
    """Instala dependências do requirements.txt"""
    if os.path.exists('requirements.txt'):
        print("📦 Instalando dependências...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("✅ Dependências instaladas")
    else:
        print("⚠️ Arquivo requirements.txt não encontrado")

def initialize_database():
    """Inicializa o banco de dados"""
    try:
        from run import app
        with app.app_context():
            from extensions import db
            from models import User, Post
            
            # Criar tabelas
            db.create_all()
            print("✅ Banco de dados inicializado")
            
            # Criar usuário admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin')
                admin.set_password('123456')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado (admin/123456)")
            else:
                print("ℹ️ Usuário admin já existe")
                
            # Criar post de exemplo
            if Post.query.count() == 0:
                post_exemplo = Post(
                    titulo="Bem-vindo ao Mente Magna!",
                    conteudo="""<h2>Seu portal de tecnologia está funcionando!</h2>
                    
<p>Este é um post de exemplo para demonstrar o funcionamento do blog. 
Você pode editá-lo ou excluí-lo através do painel administrativo.</p>

<h3>Próximos passos:</h3>
<ul>
<li>Acesse o painel admin em /auth/login</li>
<li>Use: admin / 123456</li>
<li>Crie seus próprios posts</li>
<li>Configure o Google AdSense</li>
<li>Personalize o conteúdo</li>
</ul>

<p><strong>Sucesso!</strong> 🚀</p>""",
                    publicado=True
                )
                db.session.add(post_exemplo)
                db.session.commit()
                print("✅ Post de exemplo criado")
                
    except ImportError as e:
        print(f"⚠️ Erro ao inicializar banco: {e}")
        print("   Execute: pip install -r requirements.txt")

def main():
    """Função principal de setup"""
    print("🚀 CONFIGURANDO MENTE MAGNA")
    print("=" * 50)
    
    # Verificações e configurações
    check_python_version()
    create_directories()
    create_env_file()
    install_requirements()
    initialize_database()
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Edite o arquivo .env com suas configurações de email")
    print("2. Execute: python run.py")
    print("3. Acesse: http://localhost:5000")
    print("4. Login admin: http://localhost:5000/auth/login")
    print("   Usuário: admin | Senha: 123456")
    print("\n🎯 PARA GOOGLE ADSENSE:")
    print("1. Substitua 'ca-pub-4115727278051485' pelo seu código")
    print("2. Configure slots de anúncios no AdSense")
    print("3. Atualize os data-ad-slot nos templates")
    
    print("\n🔗 LINKS ÚTEIS:")
    print("- Site: http://localhost:5000")
    print("- Admin: http://localhost:5000/auth/login")
    print("- Blog: http://localhost:5000/blog")
    print("- Sitemap: http://localhost:5000/sitemap.xml")

if __name__ == "__main__":
    main()