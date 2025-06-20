# fix_dependencies.py - Script para corrigir dependências problemáticas

import subprocess
import sys

def run_command(cmd):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

print("🔧 CORRIGINDO DEPENDÊNCIAS")
print("=" * 50)

# 1. Instalar python-dotenv corretamente (sem --user pois estamos em venv)
print("1️⃣ Instalando python-dotenv...")
success, out, err = run_command("pip install python-dotenv")
if success:
    print("✅ python-dotenv instalado!")
else:
    print(f"⚠️ Problema: {err}")

print("\n🎯 Teste manual:")
print("pip install python-dotenv")

print("\n💡 Se não funcionar, vamos usar versão sem dotenv!")