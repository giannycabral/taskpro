"""
Modelo de Anexo
"""
from datetime import datetime
from flask import current_app
import os
from app import db

class Anexo(db.Model):
    """
    Modelo representando um anexo de arquivo em uma tarefa.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)  # Nome original do arquivo
    caminho_arquivo = db.Column(db.String(500), nullable=False)  # Caminho para o arquivo no servidor
    tipo_arquivo = db.Column(db.String(100), nullable=True)  # MIME type do arquivo
    tamanho = db.Column(db.Integer, nullable=True)  # Tamanho em bytes
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Os relacionamentos são definidos nas classes Tarefa e Usuario
    
    def caminho_completo(self):
        """
        Retorna o caminho completo para o arquivo no sistema
        
        Returns:
            str: Caminho absoluto para o arquivo
        """
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.caminho_arquivo)
    
    def to_dict(self):
        """
        Converte o anexo para um dicionário
        
        Returns:
            dict: Representação do anexo como dicionário
        """
        return {
            'id': self.id,
            'nome_arquivo': self.nome_arquivo,
            'tipo_arquivo': self.tipo_arquivo,
            'tamanho': self.tamanho,
            'data_upload': self.data_upload.strftime('%Y-%m-%d %H:%M:%S'),
            'tarefa_id': self.tarefa_id,
            'usuario_id': self.usuario_id
        }
    
    def __repr__(self):
        return f'<Anexo {self.nome_arquivo} para tarefa {self.tarefa_id}>'
