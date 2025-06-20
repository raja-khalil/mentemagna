#!/usr/bin/env python3
"""
Script para corrigir erro do blog
Execute: python fix_blog.py
"""

import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'temp-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    
    return app

def fix_database():
    """Adiciona campos faltantes na tabela posts"""
    print("🔧 Corrigindo banco de dados...")
    
    db_path = os.path.join('instance', 'database.db')
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar se colunas já existem
        cursor.execute("PRAGMA table_info(posts)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Colunas existentes: {columns}")
        
        # Adicionar colunas faltantes
        new_columns = [
            ("data_atualizacao", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("meta_description", "TEXT"),
            ("keywords", "TEXT"),
            ("views", "INTEGER DEFAULT 0"),
            ("likes", "INTEGER DEFAULT 0")
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE posts ADD COLUMN {column_name} {column_type}")
                    print(f"✅ Adicionada coluna: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"⚠️ Erro ao adicionar {column_name}: {e}")
        
        # Atualizar data_atualizacao para posts existentes
        cursor.execute("UPDATE posts SET data_atualizacao = data_criacao WHERE data_atualizacao IS NULL")
        
        conn.commit()
        print("✅ Banco de dados corrigido!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_categories_table():
    """Cria tabela de categorias se não existir"""
    print("📂 Criando tabela de categorias...")
    
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Criar tabela categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                slug VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                color VARCHAR(7) DEFAULT '#007bff',
                icon VARCHAR(50) DEFAULT '📝',
                is_active BOOLEAN DEFAULT 1,
                order_index INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Criar tabela de associação
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_categories (
                post_id INTEGER,
                category_id INTEGER,
                PRIMARY KEY (post_id, category_id),
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Inserir categorias padrão
        categories = [
            ('Inteligência Artificial', 'inteligencia-artificial', 'Artigos sobre IA e Machine Learning', '#e74c3c', '🤖'),
            ('Programação', 'programacao', 'Tutoriais de programação e desenvolvimento', '#3498db', '💻'),
            ('Web Development', 'web-development', 'Desenvolvimento web e frameworks', '#2ecc71', '🌐'),
            ('Ferramentas', 'ferramentas', 'Ferramentas úteis e utilitários', '#f39c12', '🔧')
        ]
        
        for name, slug, desc, color, icon in categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, slug, description, color, icon)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, slug, desc, color, icon))
        
        conn.commit()
        print("✅ Categorias criadas!")
        
    except Exception as e:
        print(f"❌ Erro ao criar categorias: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    print("🚀 CORREÇÃO DO BLOG MENTEMAGNA")
    print("=" * 50)
    
    # Criar diretório instance se não existir
    os.makedirs('instance', exist_ok=True)
    
    # Corrigir banco
    fix_database()
    
    # Criar categorias
    create_categories_table()
    
    print("\n✅ CORREÇÃO CONCLUÍDA!")
    print("🎯 Agora execute: python run.py")