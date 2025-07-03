"""
Modelo de Compartilhamento de Tarefas
"""
from datetime import datetime
from app import db

class TarefaCompartilhada(db.Model):
    """
    Modelo representando o compartilhamento de uma tarefa entre usuários.
    """
    __tablename__ = 'tarefa_compartilhada'
    
    id = db.Column(db.Integer, primary_key=True)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)
    proprietario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario_compartilhado_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_compartilhamento = db.Column(db.DateTime, default=datetime.utcnow)
    permissao_edicao = db.Column(db.Boolean, default=False)
    
    # Os relacionamentos são definidos nas classes Tarefa e Usuario para evitar
    # referências circulares
    
    def to_dict(self):
        """
        Converte o compartilhamento para um dicionário
        
        Returns:
            dict: Representação do compartilhamento como dicionário
        """
        return {
            'id': self.id,
            'tarefa_id': self.tarefa_id,
            'proprietario_id': self.proprietario_id,
            'usuario_compartilhado_id': self.usuario_compartilhado_id,
            'data_compartilhamento': self.data_compartilhamento.strftime('%Y-%m-%d %H:%M:%S'),
            'permissao_edicao': self.permissao_edicao
        }
    
    def __repr__(self):
        return f'<TarefaCompartilhada {self.tarefa_id} de {self.proprietario_id} para {self.usuario_compartilhado_id}>'
