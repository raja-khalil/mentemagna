import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class BaseConfig:
    """
    Configurações base aplicáveis a todos os ambientes.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'segredo-padrao')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de e-mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    # CKEditor
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload'
    CKEDITOR_HEIGHT = 400

class DevelopmentConfig(BaseConfig):
    """
    Configurações específicas para desenvolvimento.
    """
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    )
    CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'instance', 'uploads')

class ProductionConfig(BaseConfig):
    """
    Configurações específicas para produção.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'database.db')}"
    )
    CKEDITOR_UPLOAD_PATH = os.getenv(
        'CKEDITOR_UPLOAD_PATH',
        os.path.join(os.getcwd(), 'instance', 'uploads')
    )

# Mapeamento de ambientes para fácil configuração
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
