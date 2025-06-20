#!/usr/bin/env python3
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
