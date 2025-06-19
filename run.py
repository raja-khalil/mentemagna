# run.py
import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, mail, ckeditor  # sem Flask-Migrate aqui
from routes.main import main_bp
from routes.blog import blog_bp
from admin.routes import admin_bp

def create_app():
    # carrega variáveis de ambiente
    load_dotenv()

    # instancia Flask apontando para instance/
    app = Flask(
        __name__,
        instance_relative_config=True
    )

    # garante que a pasta instance/ exista
    os.makedirs(app.instance_path, exist_ok=True)

    # --- Configurações ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'segredo-padrao')
    # caminho ABSOLUTO pro banco dentro de instance/
    db_path = os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração de Email
    app.config['MAIL_SERVER']   = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT']     = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS']  = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    # Configuração do CKEditor
    app.config['CKEDITOR_SERVE_LOCAL']   = True
    app.config['CKEDITOR_FILE_UPLOADER'] = 'admin.upload'
    upload_path = os.path.join(app.instance_path, 'uploads')
    app.config['CKEDITOR_UPLOAD_PATH'] = upload_path
    os.makedirs(upload_path, exist_ok=True)

    # --- Inicializa extensões ---
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)

    # --- Registra blueprints ---
    app.register_blueprint(main_bp)                 # /, /sobre, /contato…
    app.register_blueprint(blog_bp, url_prefix='/blog')  # /blog, /blog/<slug>
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

app = create_app()

if __name__ == '__main__':
    # cria o banco/tabelas caso não existam
    with app.app_context():
        db.create_all()
        print('[✅] Banco criado/verificado em', os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'][10:]))
    app.run(debug=True)
