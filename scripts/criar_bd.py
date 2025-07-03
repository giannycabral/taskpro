#!/usr/bin/env python
"""
Script para criar e popular o banco de dados com dados iniciais
"""
import os, sys
import shutil
from datetime import datetime, date, timedelta

# Adicionar o diretório raiz ao path para importações
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from app import create_app, db
from app.models import Usuario, Categoria, Tarefa, Anexo, TarefaCompartilhada, Notificacao

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
        
        # Criar um segundo usuário para testar compartilhamento
        usuario_teste2 = Usuario(nome="Outro Usuário", email="outro@exemplo.com")
        usuario_teste2.set_senha("123456")
        db.session.add(usuario_teste2)
        
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
        
        # Criar uma tarefa compartilhada
        tarefa_compartilhada = TarefaCompartilhada(
            tarefa_id=tarefas[3].id,  # "Planejar próximo trimestre"
            proprietario_id=usuario_teste.id,
            usuario_compartilhado_id=usuario_teste2.id,
            permissao_edicao=True
        )
        db.session.add(tarefa_compartilhada)
        
        # Criar uma notificação
        notificacao = Notificacao(
            usuario_id=usuario_teste2.id,
            tipo='compartilhamento',
            conteudo=f"Usuário Teste compartilhou uma tarefa com você: '{tarefas[3].conteudo}'",
            referencia_id=tarefas[3].id
        )
        db.session.add(notificacao)
        
        db.session.commit()
        
        print("Banco de dados criado com sucesso!")
        print("Usuário de teste criado:")
        print("- Email: teste@exemplo.com")
        print("- Senha: 123456")
        print("Segundo usuário criado para testar compartilhamento:")
        print("- Email: outro@exemplo.com")
        print("- Senha: 123456")

if __name__ == "__main__":
    criar_bd()
