"""
Modelo de Tarefa
"""
from datetime import datetime, date
from app import db

class Tarefa(db.Model):
    """
    Modelo representando uma tarefa.
    
    Attributes:
        id (int): Identificador único da tarefa
        conteudo (str): Descrição da tarefa
        concluida (bool): Indica se a tarefa foi concluída
        data_criacao (datetime): Data e hora de criação da tarefa
        data_vencimento (date, optional): Data de vencimento da tarefa
        usuario_id (int): ID do usuário proprietário da tarefa
        categoria_id (int, optional): ID da categoria da tarefa
        notas (str, optional): Notas detalhadas da tarefa
    """
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.Date, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    
    # Relacionamentos
    anexos = db.relationship(
        'Anexo', 
        backref='tarefa', 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    
    # Relacionamentos para compartilhamento
    # Evita dependências circulares usando strings para nomes de tabelas/colunas
    compartilhamentos = db.relationship(
        'TarefaCompartilhada',
        foreign_keys='TarefaCompartilhada.tarefa_id',
        backref=db.backref('tarefa', lazy=True),
        lazy=True, 
        cascade="all, delete-orphan",
        overlaps="compartilhamentos_recebidos,tarefa"
    )
    
    compartilhamentos_recebidos = db.relationship(
        'TarefaCompartilhada',
        primaryjoin="Tarefa.id == TarefaCompartilhada.tarefa_id",
        viewonly=True,
        overlaps="compartilhamentos,tarefa"
    )
    
    def __repr__(self):
        return f'<Tarefa {self.conteudo}>'

    def to_dict(self):
        """
        Converte a tarefa para um dicionário, útil para APIs
        
        Returns:
            dict: Representação da tarefa como dicionário
        """
        return {
            'id': self.id,
            'conteudo': self.conteudo,
            'concluida': self.concluida,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'data_vencimento': self.data_vencimento.strftime('%Y-%m-%d') if self.data_vencimento else None,
            'usuario_id': self.usuario_id,
            'categoria_id': self.categoria_id,
            'notas': self.notas
        }
    
    @property
    def status_vencimento(self):
        """
        Retorna o status de vencimento da tarefa: 'normal', 'proximo' ou 'vencida'
        
        Returns:
            str: Status de vencimento da tarefa
        """
        if not self.data_vencimento:
            return 'normal'
        
        hoje = date.today()
        dias_restantes = (self.data_vencimento - hoje).days
        
        if dias_restantes < 0:
            return 'vencida'
        elif dias_restantes <= 3:
            return 'proxima'
        else:
            return 'normal'
