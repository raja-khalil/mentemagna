# run.py
import os
from flask import Flask
from flask_mail import Mail
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from models import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Configuração correta para CKEditor uploads
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'admin.upload'  # função na blueprint
app.config['CKEDITOR_UPLOAD_PATH'] = 'static/uploads'

mail = Mail(app)
ckeditor = CKEditor(app)

db.init_app(app)

from routes.main import main_bp
from routes.blog import blog_bp
from admin.routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
