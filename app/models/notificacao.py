"""
Modelo de Notificação
"""
from datetime import datetime
from app import db

class Notificacao(db.Model):
    """
    Modelo representando uma notificação para o usuário.
    """
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'compartilhamento', 'vencimento', etc.
    conteudo = db.Column(db.String(500), nullable=False)
    referencia_id = db.Column(db.Integer, nullable=True)  # ID da tarefa ou compartilhamento relacionado
    lida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # O relacionamento está definido na classe Usuario
    
    def to_dict(self):
        """
        Converte a notificação para um dicionário
        
        Returns:
            dict: Representação da notificação como dicionário
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'conteudo': self.conteudo,
            'referencia_id': self.referencia_id,
            'lida': self.lida,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Notificacao {self.tipo} para {self.usuario_id}>'
