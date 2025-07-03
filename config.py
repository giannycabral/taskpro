import os

class Config:
    """Configurações base"""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limite

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tarefas.db'
    
class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tarefas.db')

class TestConfig(Config):
    """Configurações de teste"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usar banco de dados em memória para testes
    WTF_CSRF_ENABLED = False  # Desabilitar proteção CSRF para facilitar os testes

# Configuração para mapeamento de ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
