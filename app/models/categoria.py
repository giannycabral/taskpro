"""
Modelo de Categoria
"""
from app import db

class Categoria(db.Model):
    """
    Modelo representando uma categoria de tarefas.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Relacionamentos
    tarefas = db.relationship('Tarefa', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'
        
    def to_dict(self):
        """
        Converte a categoria para um dicionário
        
        Returns:
            dict: Representação da categoria como dicionário
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'usuario_id': self.usuario_id,
            'tarefas_count': len(self.tarefas)
        }
