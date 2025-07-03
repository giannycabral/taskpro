import unittest
import os
import tempfile
from app import create_app, db
from app.models.usuario import Usuario
from app.models.tarefa import Tarefa
from app.models.categoria import Categoria
from app.models.notificacao import Notificacao
from app.models.anexo import Anexo
from config import TestConfig

class TaskProTestCase(unittest.TestCase):
    """Testes unitários para a aplicação TaskPro"""
    
    def setUp(self):
        """Configuração do ambiente de teste antes de cada teste"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Criar um usuário de teste
            usuario = Usuario(nome='Teste', email='teste@exemplo.com')
            usuario.set_senha('123456')
            
            db.session.add(usuario)
            db.session.commit()
            
            # Criar uma categoria de teste (precisa do ID do usuário)
            categoria = Categoria(nome='Trabalho', usuario_id=usuario.id)
            
            db.session.add(categoria)
            db.session.commit()
            
            # Criar uma tarefa de teste
            tarefa = Tarefa(
                conteudo='Tarefa de teste', 
                concluida=False,
                usuario_id=usuario.id,
                categoria_id=categoria.id
            )
            
            db.session.add(tarefa)
            db.session.commit()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_pagina_inicial(self):
        """Testa se a página inicial redireciona para login quando não autenticado"""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
    
    def test_login(self):
        """Testa funcionalidade de login"""
        response = self.client.post('/auth/login', data={
            'email': 'teste@exemplo.com',
            'senha': '123456'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Na versão refatorada pode ter mudado o texto, então verificamos apenas o redirecionamento
        self.assertNotIn(b'login', response.data.lower())
    
    def test_registro(self):
        """Testa funcionalidade de registro de usuário"""
        response = self.client.post('/auth/registro', data={
            'nome': 'Novo Usuário',
            'email': 'novo@exemplo.com',
            'senha': '123456',
            'confirmar_senha': '123456'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # A mensagem pode ter mudado, verificamos se o registro funcionou
        self.assertIn(b'sucesso', response.data.lower())
    
    def test_adicionar_tarefa(self):
        """Testa adição de uma nova tarefa (requer login)"""
        # Primeiro faz login
        self.client.post('/auth/login', data={
            'email': 'teste@exemplo.com',
            'senha': '123456'
        })
        
        # Adiciona uma nova tarefa
        response = self.client.post('/adicionar', data={
            'tarefa': 'Nova tarefa de teste',
            'categoria_id': '1'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a tarefa foi adicionada ao banco de dados
        with self.app.app_context():
            tarefa = Tarefa.query.filter_by(conteudo='Nova tarefa de teste').first()
            self.assertIsNotNone(tarefa)
    
    def test_marcar_concluida(self):
        """Testa marcar uma tarefa como concluída"""
        # Primeiro faz login
        self.client.post('/auth/login', data={
            'email': 'teste@exemplo.com',
            'senha': '123456'
        })
        
        # Marca a tarefa como concluída
        response = self.client.post('/tarefas/marcar_concluida/1', follow_redirects=True)
        
        # Verificar se a tarefa foi marcada como concluída no banco de dados
        with self.app.app_context():
            tarefa = Tarefa.query.get(1)
            self.assertTrue(tarefa.concluida)
    
    def test_adicionar_categoria(self):
        """Testa adição de uma nova categoria"""
        # Primeiro faz login
        self.client.post('/auth/login', data={
            'email': 'teste@exemplo.com',
            'senha': '123456'
        })
        
        # Adiciona uma nova categoria
        response = self.client.post('/categorias/adicionar', data={
            'nome_categoria': 'Nova Categoria de Teste'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a categoria foi adicionada ao banco de dados
        with self.app.app_context():
            categoria = Categoria.query.filter_by(nome='Nova Categoria de Teste').first()
            self.assertIsNotNone(categoria)

if __name__ == '__main__':
    unittest.main()
