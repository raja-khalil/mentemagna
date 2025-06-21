#!/usr/bin/env python3
"""
Script de Inicialização da Aplicação Mente Magna
Execute este arquivo para preparar tudo automaticamente
"""

import os
import sys

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        'instance',
        'static/uploads',
        'static/img',
        'static/css',
        'static/js',
        'backups',
        'reports'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Diretório criado: {directory}")

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        env_content = '''# Configurações do Mente Magna
FLASK_ENV=development
SECRET_KEY=dev-key-change-in-production

# Configurações de Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app

# Google AdSense (opcional)
GOOGLE_ADSENSE_CLIENT=ca-pub-seu-codigo-aqui
'''
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
        print("⚠️ IMPORTANTE: Configure suas credenciais no arquivo .env!")
    else:
        print("ℹ️ Arquivo .env já existe")

def install_dependencies():
    """Instala dependências"""
    print("📦 Instalando dependências...")
    os.system(f"{sys.executable} -m pip install --upgrade pip")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    print("✅ Dependências instaladas")

def initialize_database():
    """Inicializa banco de dados"""
    try:
        from run import create_app
        from extensions import db
        from models import User, Post
        
        app = create_app()
        with app.app_context():
            # Criar tabelas
            db.create_all()
            print("✅ Banco de dados inicializado")
            
            # Criar usuário admin
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
                
            # Criar post de exemplo se não houver posts
            if Post.query.count() == 0:
                post_exemplo = Post(
                    titulo="Bem-vindo ao Mente Magna!",
                    conteudo="""<h2>Seu portal de tecnologia está funcionando!</h2>
                    
<p>Este é um post de exemplo para demonstrar o funcionamento do blog. 
Você pode editá-lo ou excluí-lo através do painel administrativo.</p>

<h3>Próximos passos:</h3>
<ul>
<li>Acesse o painel admin em <a href="/auth/login">/auth/login</a></li>
<li>Use: <strong>admin</strong> / <strong>123456</strong></li>
<li>Crie seus próprios posts</li>
<li>Configure o Google AdSense</li>
<li>Personalize o conteúdo</li>
</ul>

<p><strong>Sucesso!</strong> 🚀</p>""",
                    resumo="Post de exemplo do Mente Magna para demonstrar o funcionamento do blog.",
                    publicado=True
                )
                db.session.add(post_exemplo)
                db.session.commit()
                print("✅ Post de exemplo criado")
                
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")

def main():
    """Função principal"""
    print("🚀 INICIALIZANDO MENTE MAGNA")
    print("=" * 50)
    
    try:
        create_directories()
        create_env_file()
        install_dependencies()
        initialize_database()
        
        print("\n" + "=" * 50)
        print("✅ INICIALIZAÇÃO CONCLUÍDA!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Configure o arquivo .env com suas credenciais")
        print("2. Execute: python run.py")
        print("3. Acesse: http://localhost:5000")
        print("4. Admin: http://localhost:5000/auth/login")
        print("   Usuário: admin | Senha: 123456")
        print("\n🎯 TUDO PRONTO! Sua aplicação está funcionando!")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("Verifique se todas as dependências estão instaladas")

if __name__ == "__main__":
    main()