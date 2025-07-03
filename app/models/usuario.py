"""
Modelo de Usuário

Este módulo define o modelo de usuário para a aplicação TaskPro.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    """
    Modelo representando um usuário do sistema.
    
    Attributes:
        id (int): Identificador único do usuário
        nome (str): Nome do usuário
        email (str): Email do usuário (único)
        senha_hash (str): Hash da senha do usuário
        data_registro (datetime): Data e hora do registro do usuário
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos principais
    tarefas = db.relationship(
        'Tarefa', 
        backref='proprietario', 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    categorias = db.relationship(
        'Categoria', 
        backref='usuario', 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    notificacoes = db.relationship(
        'Notificacao', 
        backref='usuario_ref', 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    anexos = db.relationship(
        'Anexo', 
        backref='usuario', 
        lazy=True
    )
    
    # Relacionamentos para tarefas compartilhadas
    # Uso de strings para evitar dependências circulares
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
