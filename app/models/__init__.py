"""
Módulo de modelos do TaskPro
"""
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.tarefa import Tarefa
from app.models.compartilhamento import TarefaCompartilhada
from app.models.notificacao import Notificacao
from app.models.anexo import Anexo

# Exportar todos os modelos para fácil importação
__all__ = ['Usuario', 'Categoria', 'Tarefa', 'TarefaCompartilhada', 'Notificacao', 'Anexo']
