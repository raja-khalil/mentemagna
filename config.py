import os
from pathlib import Path

# Carregar .env se disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    """Configuração simples que funciona"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'mente-magna-secret-2025')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLite com caminho absoluto
    BASE_DIR = Path(__file__).parent.absolute()
    INSTANCE_DIR = BASE_DIR / 'instance'
    DATABASE_PATH = INSTANCE_DIR / 'database.db'
    
    # Garantir que o diretório existe
    INSTANCE_DIR.mkdir(exist_ok=True)
    
    # URI do banco
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = str(BASE_DIR / 'static' / 'uploads')

# Configurações por ambiente
config = {
    'development': Config,
    'production': Config,
    'default': Config,
}
