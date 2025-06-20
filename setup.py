#!/usr/bin/env python3
"""
Script de configuração inicial do MenteMagna
Execute: python setup.py
"""

import os
import sys
from getpass import getpass

def criar_env():
    """Cria arquivo .env com configurações básicas"""
    print("🔧 Configurando arquivo .env...")
    
    # Verificar se .env já existe
    if os.path.exists('.env'):
        resposta = input("Arquivo .env já existe. Sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("⏭️ Pulando configuração .env")
            return
    
    # Coletar informações
    print("\n📧 Configuração de E-mail para formulário de contato:")
    print("(Você pode usar Gmail com App Password)")
    
    mail_username = input("Email (ex: seu@gmail.com): ").strip()
    mail_password = getpass("Senha do email/App Password: ").strip()
    
    # Gerar chave secreta
    import secrets
    secret_key = secrets.token_hex(32)
    
    # Criar conteúdo do .env
    env_content = f"""# Configurações do MenteMagna
FLASK_ENV=development
SECRET_KEY={secret_key}

# Configurações de Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME={mail_username}
MAIL_PASSWORD={mail_password}

# Banco de dados (SQLite para desenvolvimento)
DATABASE_URL=sqlite:///instance/database.db
"""
    
    # Escrever arquivo
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado com sucesso!")

def instalar_dependencias():
    """Instala dependências do requirements.txt"""
    print("\n📦 Instalando dependências...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Arquivo requirements.txt não encontrado!")
        return False
    
    try:
        os.system('pip install -r requirements.txt')
        print("✅ Dependências instaladas!")
        return True
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def configurar_banco():
    """Inicializa banco de dados"""
    print("\n🗄️ Configurando banco de dados...")
    
    try:
        # Importar aqui para evitar erro se deps não estiverem instaladas
        from run import create_app
        from extensions import db
        from models import User
        
        app = create_app()
        
        with app.app_context():
            # Criar tabelas
            db.create_all()
            print("✅ Tabelas criadas!")
            
            # Verificar se já existe usuário admin
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("ℹ️ Usuário admin já existe")
                return True
            
            # Criar usuário administrador
            print("\n👤 Criando usuário administrador:")
            username = input("Nome de usuário (padrão: admin): ").strip()
            if not username:
                username = 'admin'
            
            password = getpass("Senha do administrador: ").strip()
            if not password:
                print("❌ Senha não pode estar vazia!")
                return False
            
            # Criar usuário
            admin = User(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Usuário '{username}' criado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def criar_diretorios():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    dirs = [
        'instance',
        'static/uploads',
        'migrations'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Diretório '{dir_path}' criado/verificado")

def main():
    """Função principal"""
    print("🚀 SETUP DO MENTEMAGNA")
    print("=" * 50)
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        sys.exit(1)
    
    try:
        # 1. Criar diretórios
        criar_diretorios()
        
        # 2. Configurar .env
        criar_env()
        
        # 3. Instalar dependências
        if not instalar_dependencias():
            print("❌ Falha na instalação. Verifique o requirements.txt")
            return
        
        # 4. Configurar banco
        if not configurar_banco():
            print("❌ Falha na configuração do banco")
            return
        
        print("\n" + "=" * 50)
        print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
        print("=" * 50)
        print("\n📋 Próximos passos:")
        print("1. Execute: python run.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Faça login em: http://localhost:5000/auth/login")
        print("4. Configure seu Google AdSense nos templates")
        print("\n💡 Dica: Troque 'ca-pub-XXXXXXXXXXXXXXX' pelo seu código AdSense")
        
    except KeyboardInterrupt:
        print("\n❌ Setup cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == '__main__':
    main()