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
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-temporaria-mude-em-producao')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações otimizadas para SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }

    # Configurações de e-mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'seu@email.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'sua-senha')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'seu@email.com')
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = 'static/uploads'
    
    # Configurações de segurança
    WTF_CSRF_TIME_LIMIT = None  # Sem limite de tempo para CSRF
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 dias

class DevelopmentConfig(BaseConfig):
    """
    Configurações específicas para desenvolvimento.
    """
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Banco SQLite com configurações otimizadas
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    
    # Garantir que a pasta instance existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class ProductionConfig(BaseConfig):
    """
    Configurações específicas para produção.
    """
    DEBUG = False
    
    # Opção 1: SQLite para produção simples
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'production.db')
    
    # Opção 2: PostgreSQL para produção robusta (descomente se usar)
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     'DATABASE_URL',
    #     'postgresql://usuario:senha@localhost/mentemagna'
    # )
    
    # Por padrão, usar SQLite otimizado
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{DB_PATH}"
    )
    
    # Garantir que a pasta instance existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Configurações de produção mais rigorosas
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 30,
        'pool_recycle': 3600,  # 1 hora
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 60
        }
    }

class TestingConfig(BaseConfig):
    """
    Configurações para testes automatizados.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Banco em memória para testes

# Mapeamento de ambientes para fácil configuração
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}