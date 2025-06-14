from app import app, db, Usuario, Tarefa, Categoria, Anexo
import os, shutil
from datetime import datetime, date, timedelta

# Criar o banco de dados com as tabelas corretas
with app.app_context():
    # Apaga todas as tabelas e cria novamente
    db.drop_all()
    db.create_all()
    
    # Cria um usuário de teste
    usuario_teste = Usuario(nome="Usuário Teste", email="teste@exemplo.com")
    usuario_teste.set_senha("123456")
    db.session.add(usuario_teste)
    db.session.commit()
    
    # Cria categorias de exemplo
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
    
    # Limpar a pasta de uploads
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')
    if os.path.exists(upload_folder):
        shutil.rmtree(upload_folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Cria tarefas de exemplo
    tarefas = [
        # Sem categoria e sem vencimento
        Tarefa(conteudo="Tarefa sem categoria e sem data de vencimento", 
              usuario_id=usuario_teste.id),
        
        # Tarefas de trabalho com diferentes datas
        Tarefa(conteudo="Reunião importante (vencida)", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_trabalho.id, 
              data_vencimento=ontem,
              notas="Preparar apresentação para reunião com diretores. Levar relatório semestral e dados de vendas."),
        
        Tarefa(conteudo="Enviar relatório (amanhã)", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_trabalho.id, 
              data_vencimento=amanha),
        
        Tarefa(conteudo="Planejar próximo trimestre", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_trabalho.id, 
              data_vencimento=proxima_semana,
              notas="Incluir metas de marketing, projeções financeiras e plano de contratações."),
        
        # Tarefas pessoais
        Tarefa(conteudo="Comprar presente de aniversário", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_pessoal.id, 
              data_vencimento=amanha,
              notas="Ideias: livro, relógio ou vale-presente da loja favorita."),
        
        Tarefa(conteudo="Marcar consulta médica", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_pessoal.id),
        
        # Tarefas de estudo
        Tarefa(conteudo="Estudar para prova de Python", 
              usuario_id=usuario_teste.id, 
              categoria_id=cat_estudos.id, 
              data_vencimento=proximo_mes,
              notas="Tópicos importantes: Classes, Herança, Decoradores e Gerenciamento de Exceções.\nConsultar material de apoio enviado pelo professor.")
    ]
    
    db.session.add_all(tarefas)
    db.session.commit()
    
    print("Banco de dados criado com sucesso!")
    print(f"Usuário de teste criado: {usuario_teste.email}")
    print(f"Senha: 123456")
