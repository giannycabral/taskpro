"""
Inicialização da aplicação TaskPro

Este módulo inicializa a aplicação Flask, configurações, banco de dados
e registra os blueprints.
"""
# Importações padrão
import os

# Importações de terceiros
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importações do projeto
from config import config

# Instância do SQLAlchemy
db = SQLAlchemy()

def create_app(config_name='default'):
    """
    Função factory para criar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração a ser utilizada
        
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    
    # Configuração de diretórios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicializar extensões
    db.init_app(app)
    
    with app.app_context():
        # Garantir que o banco de dados existe
        db.create_all()
    
    # Registrar blueprints
    # Nota: Importamos aqui para evitar importações circulares
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    """
    Registra todos os blueprints da aplicação
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    # Importar todos os blueprints de uma vez usando a lista centralizada
    from app.routes import blueprints
    
    # Registrar cada blueprint na aplicação
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
