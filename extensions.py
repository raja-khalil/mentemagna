from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect # <-- Adicionar esta importação

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect() # <-- Adicionar esta linha

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'