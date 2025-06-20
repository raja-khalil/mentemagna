# test_app.py - Teste simples para verificar funcionamento
import sys

print("🧪 TESTE DE DEPENDÊNCIAS")
print("=" * 40)

# Testar imports essenciais
try:
    import flask
    print(f"✅ Flask: {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask: {e}")

try:
    import flask_sqlalchemy
    print(f"✅ Flask-SQLAlchemy: {flask_sqlalchemy.__version__}")
except ImportError as e:
    print(f"❌ Flask-SQLAlchemy: {e}")

try:
    import flask_mail
    print("✅ Flask-Mail: OK")
except ImportError as e:
    print(f"❌ Flask-Mail: {e}")

try:
    import flask_ckeditor
    print("✅ Flask-CKEditor: OK")
except ImportError as e:
    print(f"❌ Flask-CKEditor: {e}")

try:
    import slugify
    print("✅ python-slugify: OK")
except ImportError as e:
    print(f"❌ python-slugify: {e}")

try:
    import flask_login
    print("✅ Flask-Login: OK")
except ImportError as e:
    print(f"❌ Flask-Login: {e}")

try:
    import wtforms
    print(f"✅ WTForms: {wtforms.__version__}")
except ImportError as e:
    print(f"❌ WTForms: {e}")

try:
    import flask_wtf
    print("✅ Flask-WTF: OK")
except ImportError as e:
    print(f"❌ Flask-WTF: {e}")

try:
    import dotenv
    print("✅ python-dotenv: OK")
except ImportError as e:
    print(f"❌ python-dotenv: {e}")

print("\n🎯 RESULTADO:")
print("=" * 40)

# Teste básico de criar uma app Flask
try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "<h1>🎉 MenteMagna Funciona!</h1><p>Site carregado com sucesso!</p>"
    
    print("✅ App Flask criada com sucesso!")
    print("🚀 Execute: python test_app.py")
    print("📱 Acesse: http://localhost:5000")
    
    # Só roda se executado diretamente
    if __name__ == '__main__':
        app.run(debug=True, port=5000)
        
except Exception as e:
    print(f"❌ Erro ao criar app: {e}")