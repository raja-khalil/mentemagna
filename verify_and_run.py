#!/usr/bin/env python3
"""
Verificação Final e Execução - Mente Magna
Script que verifica se tudo está funcionando e executa a aplicação
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

class MenteMagnaVerifier:
    """Verificador e inicializador da aplicação Mente Magna"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.base_dir = Path(__file__).parent
        
    def check_python_version(self):
        """Verifica versão do Python"""
        if sys.version_info < (3, 8):
            self.errors.append(f"Python 3.8+ necessário. Versão atual: {sys.version}")
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")
        return True
    
    def check_required_files(self):
        """Verifica se arquivos essenciais existem"""
        required_files = [
            'run.py',
            'config.py', 
            'models.py',
            'extensions.py',
            'forms.py',
            'requirements.txt',
            'routes/main.py',
            'routes/blog.py',
            'routes/auth.py',
            'admin/routes.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.base_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.errors.append(f"Arquivos essenciais faltando: {', '.join(missing_files)}")
            return False
        
        print("✅ Todos os arquivos essenciais presentes")
        return True
    
    def check_directories(self):
        """Verifica e cria diretórios necessários"""
        required_dirs = [
            'static/uploads',
            'static/img', 
            'static/css',
            'instance',
            'templates',
            'routes',
            'admin'
        ]
        
        created_dirs = []
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_path)
        
        if created_dirs:
            print(f"✅ Diretórios criados: {', '.join(created_dirs)}")
        else:
            print("✅ Todos os diretórios existem")
        
        return True
    
    def check_dependencies(self):
        """Verifica dependências Python"""
        required_packages = [
            'flask',
            'flask_sqlalchemy',
            'flask_migrate', 
            'flask_login',
            'flask_mail',
            'flask_wtf',
            'wtforms',
            'werkzeug'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.warnings.append(f"Pacotes faltando (serão instalados): {', '.join(missing_packages)}")
            return self.install_dependencies()
        
        print("✅ Todas as dependências instaladas")
        return True
    
    def install_dependencies(self):
        """Instala dependências faltantes"""
        print("📦 Instalando dependências...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ], check=True, capture_output=True, text=True)
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Erro ao instalar dependências: {e}")
            return False
    
    def check_configuration(self):
        """Verifica configurações"""
        env_file = self.base_dir / '.env'
        
        if not env_file.exists():
            print("⚠️ Arquivo .env não encontrado - será criado")
            self.create_default_env()
        
        # Verificar configuração básica
        try:
            import config
            config_obj = config.config['development']
            print("✅ Configuração carregada com sucesso")
            return True
        except Exception as e:
            self.errors.append(f"Erro na configuração: {e}")
            return False
    
    def create_default_env(self):
        """Cria arquivo .env padrão"""
        env_content = """# Configurações Mente Magna
FLASK_ENV=development
SECRET_KEY=mente-magna-dev-key-change-in-production

# Email (configure com suas credenciais)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app

# Google AdSense (substitua pelo seu código)
GOOGLE_ADSENSE_CLIENT=ca-pub-4115727278051485
"""
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
    
    def test_import_structure(self):
        """Testa se a estrutura de importação está correta"""
        try:
            # Testar importações principais
            import extensions
            import models
            import forms
            
            # Testar blueprints
            from routes.main import main_bp
            from routes.blog import blog_bp  
            from routes.auth import auth_bp
            from admin.routes import admin_bp
            
            print("✅ Estrutura de importação OK")
            return True
            
        except ImportError as e:
            self.errors.append(f"Erro de importação: {e}")
            return False
    
    def run_application(self):
        """Executa a aplicação"""
        print("\n🚀 Iniciando aplicação Mente Magna...")
        print("="*60)
        
        try:
            # Importar e executar
            import run
            app = run.create_app()
            
            print("✅ Aplicação criada com sucesso")
            print("\n🌐 INFORMAÇÕES DE ACESSO:")
            print("   URL: http://localhost:5000")
            print("   Admin: http://localhost:5000/auth/login")
            print("   Usuário: admin")
            print("   Senha: 123456")
            print("\n⏹️ Para parar: Ctrl+C")
            print("="*60)
            
            # Executar servidor
            app.run(
                debug=True,
                host='0.0.0.0',
                port=5000,
                use_reloader=True
            )
            
        except Exception as e:
            self.errors.append(f"Erro ao executar aplicação: {e}")
            return False
    
    def print_summary(self):
        """Imprime resumo da verificação"""
        print("\n" + "="*60)
        print("📋 RESUMO DA VERIFICAÇÃO - MENTE MAGNA")
        print("="*60)
        
        if self.errors:
            print("\n❌ ERROS ENCONTRADOS:")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        if self.warnings:
            print("\n⚠️ AVISOS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        if not self.errors:
            print("\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
            print("   Sua aplicação Mente Magna está pronta para uso.")
        
        print("="*60)
    
    def verify_and_run(self):
        """Executa verificação completa e inicia aplicação"""
        print("🔍 VERIFICANDO APLICAÇÃO MENTE MAGNA...")
        print("="*60)
        
        checks = [
            ("Versão do Python", self.check_python_version),
            ("Arquivos essenciais", self.check_required_files),
            ("Diretórios", self.check_directories),
            ("Dependências", self.check_dependencies),
            ("Configuração", self.check_configuration),
            ("Estrutura de importação", self.test_import_structure)
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"\n🔍 Verificando {check_name}...")
            if not check_func():
                all_passed = False
                print(f"❌ Falha em: {check_name}")
        
        self.print_summary()
        
        if all_passed:
            print("\n🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
            input("\nPressione Enter para iniciar a aplicação...")
            self.run_application()
        else:
            print("\n❌ Corrija os erros antes de continuar.")
            return False
        
        return True

def create_quick_start_script():
    """Cria script de início rápido"""
    script_content = '''#!/usr/bin/env python3
"""
Início Rápido - Mente Magna
Execute apenas: python quick_start.py
"""

if __name__ == "__main__":
    try:
        from verify_and_run import MenteMagnaVerifier
        verifier = MenteMagnaVerifier()
        verifier.verify_and_run()
    except KeyboardInterrupt:
        print("\\n👋 Aplicação finalizada pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro: {e}")
        print("\\nTente executar: python run.py")
'''
    
    with open('quick_start.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    print("✅ Script quick_start.py criado")

def main():
    """Função principal"""
    print("🎯 MENTE MAGNA - VERIFICAÇÃO E EXECUÇÃO")
    print("="*60)
    
    # Criar script de início rápido
    create_quick_start_script()
    
    # Executar verificação
    verifier = MenteMagnaVerifier()
    success = verifier.verify_and_run()
    
    if not success:
        print("\n📋 INSTRUÇÕES ALTERNATIVAS:")
        print("1. Execute: python fix_all_issues.py")
        print("2. Execute: python run.py")  
        print("3. Execute: python quick_start.py")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Verificação cancelada")
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {e}")