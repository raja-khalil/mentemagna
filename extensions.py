# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate   import Migrate
from flask_mail      import Mail
from flask_ckeditor  import CKEditor
from flask_login     import LoginManager

# já existentes
db       = SQLAlchemy()
migrate  = Migrate()
mail     = Mail()
ckeditor = CKEditor()

# nova instância para autenticação
login_manager = LoginManager()
# para onde redirecionar quando o usuário não estiver logado:
login_manager.login_view = 'auth.login'
# categoria da flash-message padrão de “login necessário”
login_manager.login_message_category = 'info'