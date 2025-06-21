#!/usr/bin/env python3
"""
Script para corrigir problemas de migração do banco de dados
Execute este script para resolver conflitos entre modelos antigos e novos
"""

import os
import sqlite3
import shutil
from datetime import datetime

def backup_current_database():
    """Cria backup do banco atual"""
    db_paths = [
        'instance/database.db',
        'mentemagna.db',
        'instance/mentemagna.db'
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"backup_before_fix_{timestamp}.db"
            shutil.copy2(db_path, backup_path)
            print(f"✅ Backup criado: {backup_path}")
            return db_path
    
    print("ℹ️ Nenhum banco existente encontrado")
    return None

def fix_database_schema():
    """Corrige o schema do banco de dados"""
    
    print("🔧 Iniciando correção do banco de dados...")
    
    # Fazer backup
    current_db = backup_current_database()
    
    # Deletar bancos existentes para forçar recriação
    db_files = [
        'instance/database.db',
        'mentemagna.db',
        'instance/mentemagna.db'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️ Removido: {db_file}")
    
    # Garantir que o diretório instance existe
    os.makedirs('instance', exist_ok=True)
    
    print("✅ Banco limpo. Agora execute 'python run.py' novamente")
    
    # Criar script de inicialização limpa
    init_script = """
from run import create_app
from extensions import db
from models import User, Post

app = create_app()
with app.app_context():
    # Criar todas as tabelas do zero
    db.create_all()
    print("✅ Tabelas criadas")
    
    # Criar usuário admin
    admin = User(username='admin')
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit()
    print("✅ Usuário admin criado")
    
    print("🎉 Banco inicializado com sucesso!")
"""
    
    with open('init_clean_db.py', 'w') as f:
        f.write(init_script)
    
    print("📝 Script de inicialização criado: init_clean_db.py")

def migrate_old_data():
    """Migra dados do banco antigo se existir backup"""
    backup_files = [f for f in os.listdir('.') if f.startswith('backup_before_fix_')]
    
    if not backup_files:
        print("ℹ️ Nenhum backup encontrado para migração")
        return
    
    latest_backup = max(backup_files)
    print(f"📥 Tentando migrar dados de: {latest_backup}")
    
    try:
        # Conectar ao backup
        conn = sqlite3.connect(latest_backup)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela users
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Colunas encontradas na tabela users: {columns}")
        
        # Migrar usuários
        if 'username' in columns and 'pw_hash' in columns:
            cursor.execute("SELECT id, username, pw_hash FROM users")
            users = cursor.fetchall()
            
            # Criar arquivo de migração manual
            migration_data = {
                'users': [],
                'posts': []
            }
            
            for user in users:
                migration_data['users'].append({
                    'id': user[0],
                    'username': user[1],
                    'pw_hash': user[2]
                })
            
            # Verificar se existe tabela posts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
            if cursor.fetchone():
                # Migrar posts
                cursor.execute("PRAGMA table_info(posts)")
                post_columns = [row[1] for row in cursor.fetchall()]
                
                select_fields = []
                if 'titulo' in post_columns:
                    select_fields.append('titulo')
                if 'conteudo' in post_columns:
                    select_fields.append('conteudo')
                if 'publicado' in post_columns:
                    select_fields.append('publicado')
                if 'slug' in post_columns:
                    select_fields.append('slug')
                if 'resumo' in post_columns:
                    select_fields.append('resumo')
                if 'imagem' in post_columns:
                    select_fields.append('imagem')
                if 'data_criacao' in post_columns:
                    select_fields.append('data_criacao')
                
                if select_fields:
                    cursor.execute(f"SELECT {', '.join(select_fields)} FROM posts")
                    posts = cursor.fetchall()
                    
                    for post in posts:
                        post_data = {}
                        for i, field in enumerate(select_fields):
                            post_data[field] = post[i]
                        migration_data['posts'].append(post_data)
            
            # Salvar dados de migração
            import json
            with open('migration_data.json', 'w') as f:
                json.dump(migration_data, f, indent=2, default=str)
            
            print(f"✅ Dados salvos em migration_data.json:")
            print(f"   👥 Usuários: {len(migration_data['users'])}")
            print(f"   📝 Posts: {len(migration_data['posts'])}")
        
        conn.close()
        
    except Exception as e:
        print(f"⚠️ Erro na migração: {e}")
        print("ℹ️ Você pode restaurar manualmente os dados mais tarde")

if __name__ == "__main__":
    print("🔧 CORREÇÃO DO BANCO DE DADOS - MENTE MAGNA")
    print("=" * 50)
    
    fix_database_schema()
    migrate_old_data()
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python run.py")
    print("2. Ou execute: python init_clean_db.py")
    print("3. Se tiver dados para restaurar, veja migration_data.json")
    print("\n🔑 Acesso admin: admin / 123456")