# extensions.py - Versão sem CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate   import Migrate
from flask_mail      import Mail
from flask_login     import LoginManager

# Extensões principais
db       = SQLAlchemy()
migrate  = Migrate()
mail     = Mail()

# Autenticação
login_manager = LoginManager()
# para onde redirecionar quando o usuário não estiver logado:
login_manager.login_view = 'auth.login'
# categoria da flash-message padrão de "login necessário"
login_manager.login_message_category = 'info'