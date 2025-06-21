#!/usr/bin/env python3
"""
Script para corrigir rapidamente os erros da aplicação
"""

import os
import sys

def create_missing_files():
    """Cria arquivos que podem estar faltando"""
    
    # Criar __init__.py nos diretórios
    init_files = [
        'routes/__init__.py',
        'admin/__init__.py',
        'admin/templates/__init__.py'
    ]
    
    for init_file in init_files:
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# __init__.py\n')
            print(f"✅ Criado: {init_file}")

def install_missing_dependencies():
    """Instala dependências que podem estar faltando"""
    dependencies = [
        'python-slugify',
        'email-validator'
    ]
    
    for dep in dependencies:
        print(f"📦 Instalando {dep}...")
        os.system(f"{sys.executable} -m pip install {dep}")

def create_simple_config():
    """Cria configuração simples"""
    config_content = '''import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-testing')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mentemagna.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/uploads'

config = {
    'development': Config,
    'production': Config,
    'default': Config
}
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("✅ config.py simplificado criado")

def main():
    """Executa todas as correções"""
    print("🔧 CORRIGINDO ERROS DA APLICAÇÃO...")
    print("=" * 50)
    
    try:
        create_missing_files()
        install_missing_dependencies()
        create_simple_config()
        
        print("\n✅ CORREÇÕES APLICADAS!")
        print("\nAgora execute:")
        print("1. python run.py")
        print("2. Acesse: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()