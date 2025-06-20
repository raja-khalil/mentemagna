#!/usr/bin/env python3
"""
Script de Migração SQLite -> PostgreSQL
Mente Magna - Sistema de Migração de Banco de Dados
"""

import os
import json
import sys
from datetime import datetime

def check_prerequisites():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando pré-requisitos...")
    
    try:
        import psycopg2
        print("✅ psycopg2 instalado")
    except ImportError:
        print("❌ psycopg2 não encontrado")
        print("   Execute: pip install psycopg2-binary")
        return False
    
    try:
        from run import create_app
        print("✅ Aplicação Flask encontrada")
    except ImportError:
        print("❌ Não foi possível importar a aplicação")
        return False
    
    return True

def export_sqlite_data():
    """Exporta dados do SQLite para JSON"""
    print("📤 Exportando dados do SQLite...")
    
    try:
        from database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        export_path = db_manager.export_data('json')
        
        if export_path:
            print(f"✅ Dados exportados para: {export_path}")
            return export_path
        else:
            print("❌ Falha ao exportar dados")
            return None
            
    except ImportError:
        print("❌ Sistema de backup não encontrado")
        return None
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")
        return None

def setup_postgresql_config():
    """Configura PostgreSQL no arquivo de configuração"""
    print("⚙️ Configurando PostgreSQL...")
    
    # Criar backup da configuração atual
    if os.path.exists('config.py'):
        backup_path = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        import shutil
        shutil.copy2('config.py', backup_path)
        print(f"🔒 Backup da configuração: {backup_path}")
    
    # Atualizar .env com configurações PostgreSQL
    env_additions = """
# Configurações PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost/mentemagna
POSTGRES_DB=mentemagna
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
"""
    
    print("📝 Atualize seu arquivo .env com as configurações PostgreSQL:")
    print(env_additions)
    
    return True

def migrate_data_to_postgresql(export_file):
    """Migra dados exportados para PostgreSQL"""
    print("📥 Migrando dados para PostgreSQL...")
    
    if not os.path.exists(export_file):
        print(f"❌ Arquivo de exportação não encontrado: {export_file}")
        return False
    
    try:
        # Carregar dados exportados
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Dados carregados:")
        for table, records in data.items():
            print(f"   {table}: {len(records)} registros")
        
        # Importar aplicação
        from run import create_app
        from extensions import db
        from models import User, Post
        
        app = create_app()
        
        with app.app_context():
            # Verificar se PostgreSQL está configurado
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if not db_uri.startswith('postgresql'):
                print("⚠️ Banco ainda configurado como SQLite")
                print("   Atualize a variável DATABASE_URL no .env")
                return False
            
            print(f"🗄️ Conectando ao PostgreSQL: {db_uri}")
            
            # Criar tabelas
            db.create_all()
            print("✅ Tabelas criadas no PostgreSQL")
            
            # Migrar usuários
            if 'users' in data:
                for user_data in data['users']:
                    # Verificar se usuário já existe
                    existing_user = User.query.filter_by(username=user_data['username']).first()
                    if not existing_user:
                        user = User(
                            username=user_data['username'],
                            pw_hash=user_data['pw_hash']
                        )
                        db.session.add(user)
                
                db.session.commit()
                print(f"✅ {len(data['users'])} usuários migrados")
            
            # Migrar posts
            if 'posts' in data:
                for post_data in data['posts']:
                    # Verificar se post já existe
                    existing_post = Post.query.filter_by(slug=post_data['slug']).first()
                    if not existing_post:
                        post = Post(
                            titulo=post_data['titulo'],
                            slug=post_data['slug'],
                            resumo=post_data.get('resumo'),
                            conteudo=post_data['conteudo'],
                            imagem=post_data.get('imagem'),
                            publicado=post_data['publicado'],
                            meta_description=post_data.get('meta_description'),
                            keywords=post_data.get('keywords'),
                            views=post_data.get('views', 0),
                            likes=post_data.get('likes', 0)
                        )
                        
                        # Definir datas se disponíveis
                        if 'data_criacao' in post_data:
                            try:
                                post.data_criacao = datetime.fromisoformat(post_data['data_criacao'].replace('Z', '+00:00'))
                            except:
                                pass
                        
                        db.session.add(post)
                
                db.session.commit()
                print(f"✅ {len(data['posts'])} posts migrados")
            
            # Verificar migração
            user_count = User.query.count()
            post_count = Post.query.count()
            
            print(f"\n📊 Migração concluída:")
            print(f"   👥 Usuários: {user_count}")
            print(f"   📝 Posts: {post_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

def verify_migration():
    """Verifica se a migração foi bem-sucedida"""
    print("🔍 Verificando migração...")
    
    try:
        from run import create_app
        from extensions import db
        from models import User, Post
        
        app = create_app()
        
        with app.app_context():
            # Verificar conexão
            db.engine.execute('SELECT 1')
            print("✅ Conexão com PostgreSQL OK")
            
            # Verificar dados
            user_count = User.query.count()
            post_count = Post.query.count()
            
            print(f"📊 Dados verificados:")
            print(f"   👥 Usuários: {user_count}")
            print(f"   📝 Posts: {post_count}")
            
            # Verificar post mais recente
            latest_post = Post.query.order_by(Post.data_criacao.desc()).first()
            if latest_post:
                print(f"   📄 Último post: {latest_post.titulo}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def main():
    """Função principal de migração"""
    print("🐘 MIGRAÇÃO SQLITE → POSTGRESQL")
    print("=" * 50)
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print("\n❌ Pré-requisitos não atendidos. Migração cancelada.")
        return
    
    # Confirmar migração
    confirm = input("\n⚠️ Esta operação irá migrar seus dados para PostgreSQL.\nContinuar? (sim/não): ")
    if confirm.lower() not in ['sim', 's', 'yes', 'y']:
        print("❌ Migração cancelada pelo usuário")
        return
    
    # Passo 1: Exportar dados SQLite
    export_file = export_sqlite_data()
    if not export_file:
        print("❌ Falha na exportação. Migração cancelada.")
        return
    
    # Passo 2: Configurar PostgreSQL
    setup_postgresql_config()
    
    # Aguardar configuração do usuário
    input("\n⏸️ Configure o PostgreSQL no .env e pressione Enter para continuar...")
    
    # Passo 3: Migrar dados
    if migrate_data_to_postgresql(export_file):
        print("\n✅ Migração concluída com sucesso!")
        
        # Passo 4: Verificar migração
        if verify_migration():
            print("\n🎉 Verificação bem-sucedida!")
            print("\n📋 Próximos passos:")
            print("1. Teste o site: python run.py")
            print("2. Verifique se todos os dados estão corretos")
            print("3. Configure backup para PostgreSQL")
        else:
            print("\n⚠️ Verificação falhou. Verifique os dados manualmente.")
    else:
        print("\n❌ Falha na migração")

if __name__ == '__main__':
    main()