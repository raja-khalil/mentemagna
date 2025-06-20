import os

# Tentar carregar dotenv se disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class BaseConfig:
    """
    Configurações base aplicáveis a todos os ambientes.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-temporaria-mude-depois')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de e-mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'seu@email.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'sua-senha')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'seu@email.com')

class DevelopmentConfig(BaseConfig):
    """
    Configurações específicas para desenvolvimento.
    """
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    )

class ProductionConfig(BaseConfig):
    """
    Configurações específicas para produção.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'database.db')}"
    )

# Mapeamento de ambientes para fácil configuração
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}