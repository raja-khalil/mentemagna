#!/usr/bin/env python3

def test_imports():
    errors = []
    
    try:
        import flask
        print("Flask OK")
    except ImportError as e:
        errors.append(f"Flask: {e}")
    
    try:
        import extensions
        print("Extensions OK")
    except ImportError as e:
        errors.append(f"Extensions: {e}")
    
    try:
        import models
        print("Models OK")
    except ImportError as e:
        errors.append(f"Models: {e}")
    
    try:
        import forms
        print("Forms OK")
    except ImportError as e:
        errors.append(f"Forms: {e}")
    
    try:
        from routes.main import main_bp
        from routes.blog import blog_bp
        from routes.auth import auth_bp
        print("Routes OK")
    except ImportError as e:
        errors.append(f"Routes: {e}")
    
    try:
        from admin.routes import admin_bp
        print("Admin OK")
    except ImportError as e:
        errors.append(f"Admin: {e}")
    
    try:
        from run import create_app
        app = create_app()
        print("App criado com sucesso")
    except Exception as e:
        errors.append(f"App creation: {e}")
    
    if errors:
        print("ERROS:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("TODOS OS TESTES PASSARAM!")
        print("Execute: python run.py")
        return True

if __name__ == "__main__":
    print("TESTANDO MENTE MAGNA...")
    print("=" * 40)
    test_imports()
