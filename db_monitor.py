#!/usr/bin/env python3
"""
Monitor de Banco de Dados - Mente Magna
Monitora saúde, performance e estatísticas do banco
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

class DatabaseMonitor:
    """Monitor para acompanhar saúde do banco de dados"""
    
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path
        self.report_dir = 'reports'
        Path(self.report_dir).mkdir(exist_ok=True)
    
    def get_database_stats(self):
        """Coleta estatísticas básicas do banco"""
        if not os.path.exists(self.db_path):
            return {"error": "Banco de dados não encontrado"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            stats = {}
            
            # Informações do arquivo
            stats['file_size_mb'] = round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
            stats['last_modified'] = datetime.fromtimestamp(os.path.getmtime(self.db_path)).isoformat()
            
            # Contagem de tabelas e registros
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            stats['tables_count'] = len(tables)
            stats['tables'] = {}
            
            for table in tables:
                table_name = table[0]
                try:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    stats['tables'][table_name] = count
                except sqlite3.OperationalError:
                    stats['tables'][table_name] = 'erro'
            
            # Informações específicas das tabelas principais
            if 'posts' in stats['tables']:
                # Posts publicados vs rascunhos
                cursor = conn.execute("SELECT COUNT(*) FROM posts WHERE publicado = 1")
                stats['posts_published'] = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM posts WHERE publicado = 0")
                stats['posts_draft'] = cursor.fetchone()[0]
                
                # Post mais recente
                cursor = conn.execute("SELECT titulo, data_criacao FROM posts ORDER BY data_criacao DESC LIMIT 1")
                recent_post = cursor.fetchone()
                if recent_post:
                    stats['latest_post'] = {
                        'title': recent_post[0],
                        'created_at': recent_post[1]
                    }
            
            # Tamanho das tabelas
            cursor = conn.execute("""
                SELECT name, 
                       (SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name=name) as indexes
                FROM sqlite_master WHERE type='table'
            """)
            
            table_info = cursor.fetchall()
            stats['table_details'] = {}
            for table_name, index_count in table_info:
                stats['table_details'][table_name] = {
                    'indexes': index_count,
                    'records': stats['tables'].get(table_name, 0)
                }
            
            conn.close()
            stats['status'] = 'healthy'
            stats['checked_at'] = datetime.now().isoformat()
            
            return stats
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error",
                "checked_at": datetime.now().isoformat()
            }
    
    def check_database_integrity(self):
        """Verifica integridade do banco de dados"""
        if not os.path.exists(self.db_path):
            return {"error": "Banco de dados não encontrado"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Verificação de integridade do SQLite
            cursor = conn.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()[0]
            
            # Verificação de chaves estrangeiras
            cursor = conn.execute("PRAGMA foreign_key_check")
            fk_errors = cursor.fetchall()
            
            # Análise do journal
            cursor = conn.execute("PRAGMA journal_mode")
            journal_mode = cursor.fetchone()[0]
            
            # Verificação de índices
            cursor = conn.execute("PRAGMA index_list(posts)")
            indexes = cursor.fetchall()
            
            conn.close()
            
            return {
                'integrity': integrity_result,
                'foreign_key_errors': len(fk_errors),
                'journal_mode': journal_mode,
                'indexes_count': len(indexes),
                'status': 'ok' if integrity_result == 'ok' and len(fk_errors) == 0 else 'warning',
                'checked_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error",
                "checked_at": datetime.now().isoformat()
            }
    
    def analyze_growth_trends(self, days=30):
        """Analisa tendências de crescimento dos dados"""
        if not os.path.exists(self.db_path):
            return {"error": "Banco de dados não encontrado"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Análise de posts por dia nos últimos X dias
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor = conn.execute("""
                SELECT DATE(data_criacao) as date, COUNT(*) as count
                FROM posts 
                WHERE data_criacao >= ?
                GROUP BY DATE(data_criacao)
                ORDER BY date
            """, (date_limit,))
            
            posts_by_date = cursor.fetchall()
            
            # Estatísticas de crescimento
            if posts_by_date:
                total_posts_period = sum(count for _, count in posts_by_date)
                avg_posts_per_day = total_posts_period / days
                
                # Últimos 7 dias vs 7 dias anteriores
                week_ago = (datetime.now() - timedelta(days=7)).isoformat()
                two_weeks_ago = (datetime.now() - timedelta(days=14)).isoformat()
                
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM posts 
                    WHERE data_criacao >= ? AND data_criacao < ?
                """, (week_ago, datetime.now().isoformat()))
                last_week = cursor.fetchone()[0]
                
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM posts 
                    WHERE data_criacao >= ? AND data_criacao < ?
                """, (two_weeks_ago, week_ago))
                prev_week = cursor.fetchone()[0]
                
                growth_rate = ((last_week - prev_week) / max(prev_week, 1)) * 100 if prev_week > 0 else 0
            else:
                total_posts_period = 0
                avg_posts_per_day = 0
                last_week = 0
                prev_week = 0
                growth_rate = 0
            
            conn.close()
            
            return {
                'period_days': days,
                'total_posts_period': total_posts_period,
                'avg_posts_per_day': round(avg_posts_per_day, 2),
                'posts_last_week': last_week,
                'posts_prev_week': prev_week,
                'growth_rate_percent': round(growth_rate, 2),
                'posts_by_date': posts_by_date,
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "analyzed_at": datetime.now().isoformat()
            }
    
    def generate_health_report(self):
        """Gera relatório completo de saúde do banco"""
        print("🔍 GERANDO RELATÓRIO DE SAÚDE DO BANCO DE DADOS...")
        
        # Coletar todas as métricas
        stats = self.get_database_stats()
        integrity = self.check_database_integrity()
        growth = self.analyze_growth_trends()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'database_stats': stats,
            'integrity_check': integrity,
            'growth_analysis': growth,
            'recommendations': self._generate_recommendations(stats, integrity, growth)
        }
        
        # Salvar relatório
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.report_dir, f'db_health_{timestamp}.json')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Relatório salvo: {report_file}")
        return report, report_file
    
    def _generate_recommendations(self, stats, integrity, growth):
        """Gera recomendações baseadas nas métricas"""
        recommendations = []
        
        # Verificar tamanho do banco
        if stats.get('file_size_mb', 0) > 100:
            recommendations.append({
                'type': 'size_warning',
                'message': 'Banco de dados está ficando grande (>100MB). Considere otimização.',
                'priority': 'medium'
            })
        
        # Verificar integridade
        if integrity.get('status') != 'ok':
            recommendations.append({
                'type': 'integrity_error',
                'message': 'Problemas de integridade detectados. Execute verificação completa.',
                'priority': 'high'
            })
        
        # Verificar crescimento
        growth_rate = growth.get('growth_rate_percent', 0)
        if growth_rate > 100:
            recommendations.append({
                'type': 'high_growth',
                'message': f'Crescimento acelerado ({growth_rate:.1f}%). Considere migração para PostgreSQL.',
                'priority': 'medium'
            })
        elif growth_rate < -50:
            recommendations.append({
                'type': 'low_activity',
                'message': 'Baixa atividade detectada. Verifique se tudo está funcionando.',
                'priority': 'low'
            })
        
        # Verificar backup
        backup_dir = 'backups'
        if os.path.exists(backup_dir):
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
            if len(backup_files) < 3:
                recommendations.append({
                    'type': 'backup_warning',
                    'message': 'Poucos backups encontrados. Configure backup automático.',
                    'priority': 'medium'
                })
        else:
            recommendations.append({
                'type': 'no_backup',
                'message': 'Sistema de backup não encontrado. Configure imediatamente.',
                'priority': 'high'
            })
        
        return recommendations
    
    def print_summary(self, report):
        """Imprime resumo do relatório na tela"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE SAÚDE DO BANCO DE DADOS")
        print("="*60)
        
        stats = report['database_stats']
        integrity = report['integrity_check']
        growth = report['growth_analysis']
        
        # Estatísticas básicas
        print(f"\n📁 ARQUIVO:")
        print(f"   Tamanho: {stats.get('file_size_mb', 'N/A')} MB")
        print(f"   Última modificação: {stats.get('last_modified', 'N/A')}")
        
        print(f"\n📊 CONTEÚDO:")
        if 'tables' in stats:
            for table, count in stats['tables'].items():
                print(f"   {table}: {count} registros")
        
        if 'posts_published' in stats:
            print(f"\n📝 POSTS:")
            print(f"   Publicados: {stats['posts_published']}")
            print(f"   Rascunhos: {stats['posts_draft']}")
        
        # Integridade
        print(f"\n🔍 INTEGRIDADE:")
        print(f"   Status: {integrity.get('integrity', 'N/A')}")
        print(f"   Erros FK: {integrity.get('foreign_key_errors', 'N/A')}")
        
        # Crescimento
        print(f"\n📈 CRESCIMENTO (últimos 30 dias):")
        print(f"   Posts no período: {growth.get('total_posts_period', 'N/A')}")
        print(f"   Média por dia: {growth.get('avg_posts_per_day', 'N/A')}")
        print(f"   Taxa de crescimento: {growth.get('growth_rate_percent', 'N/A')}%")
        
        # Recomendações
        recommendations = report['recommendations']
        if recommendations:
            print(f"\n⚠️ RECOMENDAÇÕES:")
            for rec in recommendations:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "ℹ️")
                print(f"   {priority_icon} {rec['message']}")
        else:
            print(f"\n✅ Tudo funcionando perfeitamente!")
        
        print("="*60)

def main():
    """Interface de linha de comando"""
    import sys
    
    if len(sys.argv) < 2:
        print("🔍 MONITOR DE BANCO DE DADOS - MENTE MAGNA")
        print("="*50)
        print("Comandos disponíveis:")
        print("  stats      - Estatísticas básicas")
        print("  integrity  - Verificar integridade")
        print("  growth     - Analisar crescimento")
        print("  report     - Relatório completo")
        print("  watch      - Monitoramento contínuo")
        print("\nUso: python db_monitor.py [comando]")
        return
    
    command = sys.argv[1].lower()
    monitor = DatabaseMonitor()
    
    if command == 'stats':
        stats = monitor.get_database_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif command == 'integrity':
        integrity = monitor.check_database_integrity()
        print(json.dumps(integrity, indent=2, ensure_ascii=False))
    
    elif command == 'growth':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        growth = monitor.analyze_growth_trends(days)
        print(json.dumps(growth, indent=2, ensure_ascii=False))
    
    elif command == 'report':
        report, report_file = monitor.generate_health_report()
        monitor.print_summary(report)
        print(f"\n📄 Relatório completo salvo em: {report_file}")
    
    elif command == 'watch':
        import time
        print("👀 Monitoramento contínuo iniciado (Ctrl+C para parar)")
        try:
            while True:
                stats = monitor.get_database_stats()
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Tamanho: {stats.get('file_size_mb', 0)} MB - Posts: {stats.get('tables', {}).get('posts', 0)}")
                time.sleep(60)  # Verificar a cada minuto
        except KeyboardInterrupt:
            print("\n👋 Monitoramento finalizado")
    
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == '__main__':
    main()