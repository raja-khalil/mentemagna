import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
base_dir = Path(__file__).parent.absolute()

class Config:
    """Configurações base da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-padrao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do Banco de Dados SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_dir / 'instance' / 'site.db'}"

    # Configuração de Uploads
    UPLOAD_FOLDER = base_dir / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Configuração de Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')