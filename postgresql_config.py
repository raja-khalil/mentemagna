#!/usr/bin/env python3
"""
Configuração PostgreSQL para Mente Magna
Use este arquivo para configurar PostgreSQL quando necessário
"""

import os

# Configurações PostgreSQL para adicionar ao config.py
POSTGRESQL_CONFIG = """
class PostgreSQLProductionConfig(BaseConfig):
    '''
    Configurações para PostgreSQL em produção
    '''
    DEBUG = False
    
    # PostgreSQL URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://usuario:senha@localhost/mentemagna'
    )
    
    # Configurações otimizadas para PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 0,
        'echo': False
    }
    
    # Configurações específicas PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
"""

# Instruções de instalação PostgreSQL
POSTGRESQL_SETUP_INSTRUCTIONS = """
# 🐘 GUIA DE INSTALAÇÃO POSTGRESQL

## Windows:
1. Baixar PostgreSQL: https://www.postgresql.org/download/windows/
2. Instalar com configurações padrão
3. Anotar senha do usuário 'postgres'
4. Criar banco: 
   - Abrir pgAdmin
   - Criar database 'mentemagna'

## Ubuntu/Linux:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser --interactive
sudo -u postgres createdb mentemagna

## Python Dependencies:
pip install psycopg2-binary

## Configuração .env:
DATABASE_URL=postgresql://usuario:senha@localhost/mentemagna
POSTGRES_DB=mentemagna
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

## Migração:
python migrate_to_postgresql.py
"""

def show_postgresql_info():
    """Mostra informações sobre PostgreSQL"""
    print("🐘 INFORMAÇÕES POSTGRESQL")
    print("=" * 50)
    print(POSTGRESQL_SETUP_INSTRUCTIONS)

def create_postgresql_env():
    """Cria arquivo .env com configurações PostgreSQL"""
    env_content = """# Configurações PostgreSQL - Mente Magna
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-forte-aqui
DATABASE_URL=postgresql://usuario:senha@localhost/mentemagna

# PostgreSQL específico
POSTGRES_DB=mentemagna
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha_forte
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email (mantenha suas configurações atuais)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu@email.com
MAIL_PASSWORD=sua-senha-de-app
"""
    
    with open('.env.postgresql', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env.postgresql criado")
    print("📝 Edite o arquivo e renomeie para .env quando estiver pronto")

def check_postgresql_connection():
    """Testa conexão com PostgreSQL"""
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        # Pegar URL do .env
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv('DATABASE_URL', '')
        
        if not db_url.startswith('postgresql'):
            print("❌ DATABASE_URL não configurada para PostgreSQL")
            return False
        
        # Parsear URL
        result = urlparse(db_url)
        
        # Testar conexão
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        
        print(f"✅ Conexão PostgreSQL OK")
        print(f"📊 Versão: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("❌ psycopg2 não instalado")
        print("   Execute: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Interface de linha de comando"""
    import sys
    
    if len(sys.argv) < 2:
        print("🐘 CONFIGURADOR POSTGRESQL - MENTE MAGNA")
        print("=" * 50)
        print("Comandos disponíveis:")
        print("  info       - Mostrar instruções")
        print("  create-env - Criar .env para PostgreSQL")
        print("  test       - Testar conexão")
        print("  migrate    - Executar migração")
        print("\nUso: python postgresql_config.py [comando]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'info':
        show_postgresql_info()
    
    elif command == 'create-env':
        create_postgresql_env()
    
    elif command == 'test':
        check_postgresql_connection()
    
    elif command == 'migrate':
        print("🔄 Iniciando migração...")
        os.system('python migrate_to_postgresql.py')
    
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == '__main__':
    main()