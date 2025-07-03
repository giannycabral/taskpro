from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

# Instância do SQLAlchemy
db = SQLAlchemy()

def create_app(config_name='default'):
    """Função factory para criar a aplicação Flask"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    
    # Assegurar que o diretório de uploads existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicializar extensões
    db.init_app(app)
    
    with app.app_context():
        # Garantir que o banco de dados existe
        db.create_all()
    
    # Registrar blueprints
    # Nota: Importamos aqui para evitar importações circulares
    from app.routes.auth import auth_bp
    from app.routes.tarefas import tarefas_bp
    from app.routes.categorias import categorias_bp
    from app.routes.compartilhamento import compartilhamento_bp
    from app.routes.notificacoes import notificacoes_bp
    from app.routes.anexos import anexos_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(compartilhamento_bp)
    app.register_blueprint(notificacoes_bp)
    app.register_blueprint(anexos_bp)
    
    return app
