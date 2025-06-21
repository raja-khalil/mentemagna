import os
import sys

# Adiciona o diretório da aplicação ao Python Path
sys.path.insert(0, os.path.dirname(__file__))

# Define a variável de ambiente para 'production'
os.environ['FLASK_ENV'] = 'production'

# Importa a aplicação criada pelo factory
from run import create_app

# A variável 'application' é o que o Passenger procura
application = create_app('production')