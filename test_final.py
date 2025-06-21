#!/usr/bin/env python3
"""
Teste Simples - Verifica funcionamento
"""

import os
import sys
from pathlib import Path

def test_basic_imports():
    """Testa imports básicos"""
    print("Testando imports básicos...")
    
    try:
        import flask
        print("  ✓ Flask")
    except ImportError:
        print("  ✗ Flask não encontrado")
        return False
    
    try:
        import extensions
        print("  ✓ Extensions")
    except ImportError as e:
        print(f"  ✗ Extensions: {e}")
        return False
    
    try:
        import models
        print("  ✓ Models")
    except ImportError as e:
        print(f"  ✗ Models: {e}")
        return False
    
    try:
        import forms
        print("  ✓ Forms")
    except ImportError as e:
        print(f"  ✗ Forms: {e}")
        return False
    
    return True

def test_app_creation():
    """Testa criação da aplicação"""
    print("\nTestando criação da aplicação...")
    
    try:
        from run import create_app
        app = create_app()
        print("  ✓ Aplicação criada com sucesso!")
        return True
    except Exception as e:
        print(f"  ✗ Erro ao criar aplicação: {e}")
        return False

def test_database():
    """Testa banco de dados"""
    print("\nTestando banco de dados...")
    
    try:
        # Verificar se arquivo do banco pode ser criado
        base_dir = Path(__file__).parent
        instance_dir = base_dir / 'instance'
        db_file = instance_dir / 'test.db'
        
        # Criar diretório se não existir
        instance_dir.mkdir(exist_ok=True)
        
        # Testar criação de arquivo
        with open(db_file, 'w') as f:
            f.write('test')
        
        # Remover arquivo de teste
        os.remove(db_file)
        
        print("  ✓ Banco de dados pode ser criado")
        return True
        
    except Exception as e:
        print(f"  ✗ Erro no banco de dados: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("TESTE COMPLETO - MENTE MAGNA")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_database,
        test_app_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("✓ TODOS OS TESTES PASSARAM!")
        print("\nExecute agora: python run.py")
        return True
    else:
        print("✗ Alguns testes falharam")
        print("Execute: python final_fix.py")
        return False

if __name__ == "__main__":
    main()
