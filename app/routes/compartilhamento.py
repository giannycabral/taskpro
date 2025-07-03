"""
Blueprint de compartilhamento
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import db
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.models.compartilhamento import TarefaCompartilhada
from app.models.notificacao import Notificacao
from app.utils.decorators import login_obrigatorio

# Criação do blueprint
compartilhamento_bp = Blueprint('compartilhamento', __name__, url_prefix='/compartilhamento')

@compartilhamento_bp.route('/tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
@login_obrigatorio
def compartilhar_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    
    if request.method == 'POST':
        # Recebe o email do usuário com quem compartilhar
        email_destinatario = request.form.get('email')
        permissao_edicao = 'permissao_edicao' in request.form
        
        # Verifica se o email foi fornecido
        if not email_destinatario:
            flash('Por favor, insira o email do usuário com quem deseja compartilhar a tarefa', 'erro')
            return redirect(url_for('compartilhamento.compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se o usuário existe
        destinatario = Usuario.query.filter_by(email=email_destinatario).first()
        if not destinatario:
            flash('Usuário não encontrado', 'erro')
            return redirect(url_for('compartilhamento.compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se não está tentando compartilhar consigo mesmo
        if destinatario.id == usuario_id:
            flash('Você não pode compartilhar uma tarefa consigo mesmo', 'erro')
            return redirect(url_for('compartilhamento.compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se a tarefa já está compartilhada com esse usuário
        compartilhamento_existente = TarefaCompartilhada.query.filter_by(
            tarefa_id=tarefa_id,
            proprietario_id=usuario_id,
            usuario_compartilhado_id=destinatario.id
        ).first()
        
        if compartilhamento_existente:
            # Atualiza as permissões se já estiver compartilhada
            compartilhamento_existente.permissao_edicao = permissao_edicao
            db.session.commit()
            flash(f'Tarefa já compartilhada com {destinatario.nome}. Permissões atualizadas.', 'sucesso')
            return redirect(url_for('tarefas.index'))
            
        # Cria um novo compartilhamento
        novo_compartilhamento = TarefaCompartilhada(
            tarefa_id=tarefa_id,
            proprietario_id=usuario_id,
            usuario_compartilhado_id=destinatario.id,
            permissao_edicao=permissao_edicao
        )
        
        db.session.add(novo_compartilhamento)
        
        # Cria uma notificação para o destinatário
        usuario_atual = Usuario.query.get(usuario_id)
        tipo_permissao = "com permissão de edição" if permissao_edicao else "somente para visualização"
        
        nova_notificacao = Notificacao(
            usuario_id=destinatario.id,
            tipo='compartilhamento',
            conteudo=f"{usuario_atual.nome} compartilhou uma tarefa com você ({tipo_permissao}): '{tarefa.conteudo}'",
            referencia_id=tarefa_id
        )
        
        db.session.add(nova_notificacao)
        db.session.commit()
        
        flash(f'Tarefa compartilhada com {destinatario.nome} com sucesso!', 'sucesso')
        return redirect(url_for('tarefas.index'))
        
    # Carrega a lista de usuários para o formulário de compartilhamento (exclui o usuário atual)
    usuarios = Usuario.query.filter(Usuario.id != usuario_id).all()
    
    # Carrega os compartilhamentos existentes para esta tarefa
    compartilhamentos = TarefaCompartilhada.query.filter_by(
        tarefa_id=tarefa_id,
        proprietario_id=usuario_id
    ).all()
    
    compartilhamentos_info = []
    for c in compartilhamentos:
        compartilhamentos_info.append({
            'id': c.id,
            'nome_usuario': c.usuario_compartilhado.nome,
            'email_usuario': c.usuario_compartilhado.email,
            'permissao_edicao': c.permissao_edicao,
            'data': c.data_compartilhamento.strftime('%d/%m/%Y %H:%M')
        })
    
    return render_template(
        'compartilhar_tarefa.html',
        tarefa=tarefa,
        usuarios=usuarios,
        compartilhamentos=compartilhamentos_info
    )

@compartilhamento_bp.route('/remover/<int:compartilhamento_id>', methods=['POST'])
@login_obrigatorio
def remover_compartilhamento(compartilhamento_id):
    usuario_id = session.get('usuario_id')
    
    # Busca o compartilhamento e verifica se o usuário atual é o proprietário
    compartilhamento = TarefaCompartilhada.query.filter_by(id=compartilhamento_id, proprietario_id=usuario_id).first_or_404()
    
    # Armazena o ID da tarefa para redirecionamento
    tarefa_id = compartilhamento.tarefa_id
    
    # Remove o compartilhamento
    db.session.delete(compartilhamento)
    db.session.commit()
    
    flash('Compartilhamento removido com sucesso', 'sucesso')
    return redirect(url_for('compartilhamento.compartilhar_tarefa', tarefa_id=tarefa_id))

@compartilhamento_bp.route('/tarefas')
@login_obrigatorio
def tarefas_compartilhadas():
    usuario_id = session.get('usuario_id')
    
    # Busca todas as tarefas compartilhadas com o usuário atual
    compartilhamentos = TarefaCompartilhada.query.filter_by(usuario_compartilhado_id=usuario_id).all()
    
    tarefas_compartilhadas = []
    for c in compartilhamentos:
        tarefa = c.tarefa
        proprietario = c.proprietario
        
        tarefas_compartilhadas.append({
            'tarefa': tarefa,
            'proprietario': proprietario,
            'data_compartilhamento': c.data_compartilhamento,
            'permissao_edicao': c.permissao_edicao,
            'compartilhamento_id': c.id
        })
    
    return render_template(
        'tarefas_compartilhadas.html',
        tarefas_compartilhadas=tarefas_compartilhadas
    )

@compartilhamento_bp.route('/editar/<int:compartilhamento_id>', methods=['GET', 'POST'])
@login_obrigatorio
def editar_tarefa_compartilhada(compartilhamento_id):
    usuario_id = session.get('usuario_id')
    
    # Busca o compartilhamento e verifica se o usuário tem permissão
    compartilhamento = TarefaCompartilhada.query.filter_by(
        id=compartilhamento_id, 
        usuario_compartilhado_id=usuario_id,
        permissao_edicao=True
    ).first_or_404()
    
    tarefa = compartilhamento.tarefa
    
    if request.method == 'POST':
        conteudo = request.form.get('tarefa')
        data_vencimento_str = request.form.get('data_vencimento')
        
        if conteudo:
            tarefa.conteudo = conteudo
            
            # Atualiza a data de vencimento, se fornecida
            data_vencimento = None
            if data_vencimento_str and data_vencimento_str != '':
                try:
                    data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
                    tarefa.data_vencimento = data_vencimento
                except ValueError:
                    flash('Formato de data inválido. Use YYYY-MM-DD', 'erro')
                    return redirect(url_for('compartilhamento.editar_tarefa_compartilhada', compartilhamento_id=compartilhamento_id))
            
            db.session.commit()
            flash('Tarefa compartilhada atualizada com sucesso!', 'sucesso')
            return redirect(url_for('compartilhamento.tarefas_compartilhadas'))
    
    return render_template('editar_tarefa_compartilhada.html', tarefa=tarefa, compartilhamento=compartilhamento)
