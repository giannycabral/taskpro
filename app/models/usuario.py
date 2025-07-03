"""
Modelo de Usuário
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    """
    Modelo representando um usuário do sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    tarefas = db.relationship('Tarefa', backref='proprietario', lazy=True, cascade="all, delete-orphan")
    categorias = db.relationship('Categoria', backref='usuario', lazy=True, cascade="all, delete-orphan")
    notificacoes = db.relationship('Notificacao', backref='usuario_ref', lazy=True, cascade="all, delete-orphan")
    anexos = db.relationship('Anexo', backref='usuario', lazy=True)
    
    # Relacionamentos para tarefas compartilhadas
    tarefas_compartilhadas_por_mim = db.relationship(
        'TarefaCompartilhada',
        foreign_keys='TarefaCompartilhada.proprietario_id',
        backref=db.backref('proprietario', lazy=True),
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    tarefas_compartilhadas_comigo = db.relationship(
        'TarefaCompartilhada',
        foreign_keys='TarefaCompartilhada.usuario_compartilhado_id',
        backref=db.backref('usuario_compartilhado', lazy=True),
        lazy=True
    )
    
    def set_senha(self, senha):
        """
        Define a senha criptografada para o usuário
        
        Args:
            senha (str): Senha em texto puro
        """
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        """
        Verifica se a senha fornecida coincide com a senha criptografada
        
        Args:
            senha (str): Senha em texto puro para verificação
            
        Returns:
            bool: True se a senha estiver correta, False caso contrário
        """
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
