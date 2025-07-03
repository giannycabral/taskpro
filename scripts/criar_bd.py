"""
Script para criar e popular o banco de dados com dados iniciais
"""
import os, sys
import shutil
from datetime import datetime, date, timedelta

# Adicionar o diretório raiz ao path para importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.tarefa import Tarefa
from app.models.anexo import Anexo

def criar_bd():
    """Cria o banco de dados e popula com dados iniciais"""
    app = create_app('development')
    
    with app.app_context():
        print("Criando o banco de dados...")
        # Apaga todas as tabelas e cria novamente
        db.drop_all()
        db.create_all()
        
        # Cria um usuário de teste
        print("Criando usuário de teste...")
        usuario_teste = Usuario(nome="Usuário Teste", email="teste@exemplo.com")
        usuario_teste.set_senha("123456")
        db.session.add(usuario_teste)
        db.session.commit()
        
        # Cria categorias de exemplo
        print("Criando categorias de exemplo...")
        cat_trabalho = Categoria(nome="Trabalho", usuario_id=usuario_teste.id)
        cat_pessoal = Categoria(nome="Pessoal", usuario_id=usuario_teste.id)
        cat_estudos = Categoria(nome="Estudos", usuario_id=usuario_teste.id)
        db.session.add_all([cat_trabalho, cat_pessoal, cat_estudos])
        db.session.commit()
        
        # Datas de vencimento para exemplos
        hoje = date.today()
        amanha = hoje + timedelta(days=1)
        proxima_semana = hoje + timedelta(days=7)
        ontem = hoje - timedelta(days=1)
        proximo_mes = hoje + timedelta(days=30)
        
        # Cria tarefas de exemplo
        print("Criando tarefas de exemplo...")
        tarefas = [
            Tarefa(
                conteudo="Finalizar relatório de vendas",
                data_vencimento=amanha,
                usuario_id=usuario_teste.id,
                categoria_id=cat_trabalho.id,
                notas="Incluir gráficos comparativos com o trimestre anterior."
            ),
            Tarefa(
                conteudo="Fazer compras no supermercado",
                data_vencimento=hoje,
                usuario_id=usuario_teste.id,
                categoria_id=cat_pessoal.id,
                notas="Leite, ovos, pão, frutas, verduras."
            ),
            Tarefa(
                conteudo="Estudar para a prova de matemática",
                data_vencimento=proxima_semana,
                usuario_id=usuario_teste.id,
                categoria_id=cat_estudos.id,
                notas="Capítulos 5 a 8 - Foco em álgebra linear e cálculo diferencial."
            ),
            Tarefa(
                conteudo="Pagar conta de luz",
                data_vencimento=ontem,
                usuario_id=usuario_teste.id,
                categoria_id=cat_pessoal.id,
                concluida=True
            ),
            Tarefa(
                conteudo="Preparar apresentação para reunião",
                data_vencimento=proximo_mes,
                usuario_id=usuario_teste.id,
                categoria_id=cat_trabalho.id
            )
        ]
        
        db.session.add_all(tarefas)
        db.session.commit()
        
        print("Banco de dados criado com sucesso!")
        print("Usuário de teste criado: teste@exemplo.com")
        print("Senha: 123456")

if __name__ == "__main__":
    criar_bd()
