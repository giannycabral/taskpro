"""
Módulo de rotas do TaskPro

Este módulo facilita o acesso aos blueprints do TaskPro de forma centralizada.
Facilita também o registro de blueprints no app/__init__.py.
"""
# Importação absoluta para evitar problemas ao importar este módulo de outros lugares
from app.routes.auth import auth_bp
from app.routes.tarefas import tarefas_bp
from app.routes.categorias import categorias_bp
from app.routes.compartilhamento import compartilhamento_bp
from app.routes.notificacoes import notificacoes_bp
from app.routes.anexos import anexos_bp

# Lista de todos os blueprints para facilitar importação e registro
blueprints = [
    auth_bp,
    tarefas_bp,
    categorias_bp,
    compartilhamento_bp,
    notificacoes_bp,
    anexos_bp
]

# Documentação dos blueprints
__blueprints_info__ = {
    'auth_bp': 'Gerencia autenticação de usuários (registro, login, logout)',
    'tarefas_bp': 'Gerencia operações sobre tarefas (CRUD)',
    'categorias_bp': 'Gerencia categorias de tarefas',
    'compartilhamento_bp': 'Gerencia compartilhamento de tarefas entre usuários',
    'notificacoes_bp': 'Gerencia notificações do sistema',
    'anexos_bp': 'Gerencia anexos de tarefas'
}
