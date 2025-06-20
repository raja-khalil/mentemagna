#!/usr/bin/env python3
"""
Gerenciador de Banco de Dados - Mente Magna
Sistema para backup automático e migração de dados
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    """Gerenciador de banco de dados com backup automático"""
    
    def __init__(self, app=None):
        self.app = app
        self.backup_dir = 'backups'
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Garante que o diretório de backup existe"""
        Path(self.backup_dir).mkdir(exist_ok=True)
        print(f"✅ Diretório de backup: {self.backup_dir}")
    
    def get_db_path(self):
        """Retorna o caminho do banco de dados atual"""
        if self.app:
            # Extrair caminho do SQLAlchemy URI
            uri = self.app.config['SQLALCHEMY_DATABASE_URI']
            if uri.startswith('sqlite:///'):
                return uri.replace('sqlite:///', '')
        return 'instance/database.db'
    
    def create_backup(self, backup_name=None):
        """Cria backup do banco de dados"""
        db_path = self.get_db_path()
        
        if not os.path.exists(db_path):
            print(f"⚠️ Banco de dados não encontrado: {db_path}")
            return False
        
        # Nome do backup
        if not backup_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.db"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(db_path, backup_path)
            print(f"✅ Backup criado: {backup_path}")
            
            # Criar info do backup
            info_path = backup_path.replace('.db', '_info.json')
            backup_info = {
                'created_at': datetime.now().isoformat(),
                'original_path': db_path,
                'size_bytes': os.path.getsize(backup_path),
                'version': '1.0'
            }
            
            with open(info_path, 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            return backup_path
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def list_backups(self):
        """Lista todos os backups disponíveis"""
        backups = []
        
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                backup_path = os.path.join(self.backup_dir, file)
                info_path = backup_path.replace('.db', '_info.json')
                
                backup_info = {
                    'filename': file,
                    'path': backup_path,
                    'size': os.path.getsize(backup_path),
                    'created': datetime.fromtimestamp(os.path.getctime(backup_path))
                }
                
                # Carregar info adicional se existir
                if os.path.exists(info_path):
                    try:
                        with open(info_path, 'r') as f:
                            extra_info = json.load(f)
                            backup_info.update(extra_info)
                    except:
                        pass
                
                backups.append(backup_info)
        
        # Ordenar por data de criação (mais recente primeiro)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def restore_backup(self, backup_filename):
        """Restaura um backup"""
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup não encontrado: {backup_filename}")
            return False
        
        db_path = self.get_db_path()
        
        try:
            # Criar backup do estado atual antes de restaurar
            current_backup = self.create_backup(f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
            print(f"🔄 Backup atual criado: {current_backup}")
            
            # Restaurar o backup
            shutil.copy2(backup_path, db_path)
            print(f"✅ Backup restaurado: {backup_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def export_data(self, format='json'):
        """Exporta dados do banco em formato JSON ou SQL"""
        db_path = self.get_db_path()
        
        if not os.path.exists(db_path):
            print(f"❌ Banco não encontrado: {db_path}")
            return False
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            
            if format == 'json':
                export_path = os.path.join(self.backup_dir, f"export_{timestamp}.json")
                data = {}
                
                # Exportar tabelas principais
                tables = ['users', 'posts']
                
                for table in tables:
                    try:
                        cursor = conn.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        data[table] = [dict(row) for row in rows]
                        print(f"✅ Exportada tabela {table}: {len(rows)} registros")
                    except sqlite3.OperationalError:
                        print(f"⚠️ Tabela {table} não encontrada")
                        data[table] = []
                
                # Salvar JSON
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                
                print(f"✅ Dados exportados: {export_path}")
                return export_path
            
        except Exception as e:
            print(f"❌ Erro ao exportar dados: {e}")
            return False
        finally:
            conn.close()
    
    def cleanup_old_backups(self, keep_count=10):
        """Remove backups antigos, mantendo apenas os mais recentes"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            print(f"ℹ️ Mantendo todos os {len(backups)} backups")
            return
        
        # Remover backups mais antigos
        to_remove = backups[keep_count:]
        
        for backup in to_remove:
            try:
                os.remove(backup['path'])
                # Remover arquivo de info também
                info_path = backup['path'].replace('.db', '_info.json')
                if os.path.exists(info_path):
                    os.remove(info_path)
                print(f"🗑️ Backup removido: {backup['filename']}")
            except Exception as e:
                print(f"⚠️ Erro ao remover {backup['filename']}: {e}")
        
        print(f"✅ Limpeza concluída. Mantidos {keep_count} backups")

def setup_database_with_backup(app):
    """Configura o banco com sistema de backup"""
    from extensions import db
    from models import User, Post
    
    with app.app_context():
        # Criar gerenciador de backup
        db_manager = DatabaseManager(app)
        
        # Criar backup antes de qualquer operação
        backup_path = db_manager.create_backup()
        if backup_path:
            print(f"🔒 Backup de segurança criado: {backup_path}")
        
        # Criar tabelas
        db.create_all()
        print("✅ Tabelas do banco verificadas/criadas")
        
        # Verificar dados existentes
        user_count = User.query.count()
        post_count = Post.query.count()
        
        print(f"📊 Estado atual do banco:")
        print(f"   👥 Usuários: {user_count}")
        print(f"   📝 Posts: {post_count}")
        
        # Criar usuário admin se não existir
        if user_count == 0:
            admin = User(username='admin')
            admin.set_password('123456')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado")
        
        return db_manager

# Comando para linha de comando
def main():
    """Interface de linha de comando para gerenciamento do banco"""
    import sys
    
    if len(sys.argv) < 2:
        print("🗄️ GERENCIADOR DE BANCO - MENTE MAGNA")
        print("=" * 50)
        print("Comandos disponíveis:")
        print("  backup     - Criar backup")
        print("  list       - Listar backups")
        print("  restore    - Restaurar backup")
        print("  export     - Exportar dados")
        print("  cleanup    - Limpar backups antigos")
        print("\nUso: python database_manager.py [comando]")
        return
    
    command = sys.argv[1].lower()
    db_manager = DatabaseManager()
    
    if command == 'backup':
        backup_path = db_manager.create_backup()
        if backup_path:
            print(f"✅ Backup criado com sucesso!")
        
    elif command == 'list':
        backups = db_manager.list_backups()
        if backups:
            print(f"\n📋 BACKUPS DISPONÍVEIS ({len(backups)}):")
            print("-" * 50)
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                print(f"📁 {backup['filename']}")
                print(f"   📅 Criado: {backup['created']}")
                print(f"   📏 Tamanho: {size_mb:.2f} MB")
                print()
        else:
            print("ℹ️ Nenhum backup encontrado")
    
    elif command == 'restore':
        backups = db_manager.list_backups()
        if not backups:
            print("❌ Nenhum backup disponível")
            return
        
        print("\n📋 BACKUPS DISPONÍVEIS:")
        for i, backup in enumerate(backups):
            print(f"{i+1}. {backup['filename']} ({backup['created']})")
        
        try:
            choice = int(input("\nEscolha o backup (número): ")) - 1
            if 0 <= choice < len(backups):
                confirm = input(f"Restaurar '{backups[choice]['filename']}'? (sim/não): ")
                if confirm.lower() in ['sim', 's', 'yes', 'y']:
                    db_manager.restore_backup(backups[choice]['filename'])
            else:
                print("❌ Opção inválida")
        except (ValueError, KeyboardInterrupt):
            print("❌ Operação cancelada")
    
    elif command == 'export':
        export_path = db_manager.export_data()
        if export_path:
            print(f"✅ Dados exportados com sucesso!")
    
    elif command == 'cleanup':
        try:
            keep = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            db_manager.cleanup_old_backups(keep)
        except ValueError:
            print("❌ Número inválido para manter backups")
    
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == '__main__':
    main()