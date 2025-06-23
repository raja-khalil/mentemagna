import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
base_dir = Path(__file__).parent.absolute()

class Config:
    """Configurações base da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-forte-e-dificil-de-adivinhar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de Uploads
    UPLOAD_FOLDER = os.path.join(base_dir, 'static')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Configuração de Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    # Configuração do AdSense
    GOOGLE_ADSENSE_CLIENT = os.environ.get('GOOGLE_ADSENSE_CLIENT', 'ca-pub-XXXXXXXXXXXXXXX')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'instance', 'dev.db')}"

class ProductionConfig(Config):
    """Configurações para produção."""
    DEBUG = False
    # ================== CONFIGURAÇÃO RESTAURADA PARA PRODUÇÃO ==================
    # Esta linha foi descomentada para usar a variável de ambiente DATABASE_URL do Render.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(base_dir, 'instance', 'prod.db')}"
    # ===========================================================================

class TestingConfig(Config):
    """Configurações para testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestingConfig
)