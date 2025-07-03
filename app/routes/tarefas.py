"""
Blueprint de tarefas

Este módulo contém as rotas relacionadas à gestão de tarefas:
- Listagem de tarefas
- Adição de novas tarefas
- Edição de tarefas existentes
- Exclusão de tarefas
- Marcação de tarefas como concluídas
- Visualização de detalhes de tarefas
"""
# Importações do Flask
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify
)

# Importações de bibliotecas padrão
from datetime import datetime

# Importações da aplicação
from app import db
from app.utils.decorators import login_obrigatorio

# Importações de modelos (agrupadas por funcionalidade)
from app.models.tarefa import Tarefa
from app.models.categoria import Categoria
from app.models.compartilhamento import TarefaCompartilhada
from app.models.notificacao import Notificacao

# Criação do blueprint
tarefas_bp = Blueprint('tarefas', __name__)

@tarefas_bp.route('/')
@login_obrigatorio
def index():
    usuario_id = session.get('usuario_id')
    categorias = Categoria.query.filter_by(usuario_id=usuario_id).all()
    
    # Obter parâmetros de filtro e ordenação
    filtro_status = request.args.get('status', 'todas')
    ordem = request.args.get('ordem', 'criacao')
    
    # Iniciar query básica
    query = Tarefa.query.filter_by(usuario_id=usuario_id)
    
    # Aplicar filtros de status
    if filtro_status == 'concluidas':
        query = query.filter_by(concluida=True)
    elif filtro_status == 'pendentes':
        query = query.filter_by(concluida=False)
    
    # Aplicar ordenação
    if ordem == 'vencimento':
        # Ordenar tarefas com vencimento primeiro, as sem vencimento depois
        query = query.order_by(
            (Tarefa.data_vencimento == None).asc(),  # Coloca NULL (sem data) por último
            Tarefa.data_vencimento.asc(),            # Ordena por data crescente
            Tarefa.data_criacao.desc()               # Se mesma data, mostra mais recente primeiro
        )
    elif ordem == 'vencimento_desc':
        # Ordenar por data de vencimento decrescente (mais distante primeiro)
        query = query.order_by(
            (Tarefa.data_vencimento == None).asc(),  # Coloca NULL (sem data) por último 
            Tarefa.data_vencimento.desc(),           # Ordena por data decrescente
            Tarefa.data_criacao.desc()               # Se mesma data, mostra mais recente primeiro
        )
    elif ordem == 'criacao_desc':
        # Mais antigas primeiro
        query = query.order_by(Tarefa.data_criacao.asc())
    else:  # criacao (padrão)
        # Mais recentes primeiro
        query = query.order_by(Tarefa.data_criacao.desc())
    
    # Executar a consulta
    tarefas = query.all()
    
    # Agrupar tarefas por categoria
    tarefas_por_categoria = {}
    for categoria in categorias:
        tarefas_por_categoria[categoria.nome] = [t for t in tarefas if t.categoria_id == categoria.id]
    tarefas_sem_categoria = [t for t in tarefas if t.categoria_id is None]
    
    # Verificar quantas tarefas foram compartilhadas com o usuário
    contagem_compartilhadas = TarefaCompartilhada.query.filter_by(usuario_compartilhado_id=usuario_id).count()
    
    # Verificar quantas notificações não lidas o usuário possui
    contagem_notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id, lida=False).count()
    
    return render_template(
        'index.html',
        tarefas=tarefas,
        usuario_nome=session.get('usuario_nome'),
        categorias=categorias,
        tarefas_por_categoria=tarefas_por_categoria,
        contagem_compartilhadas=contagem_compartilhadas,
        contagem_notificacoes=contagem_notificacoes,
        tarefas_sem_categoria=tarefas_sem_categoria,
        filtro_status=filtro_status,
        ordem=ordem
    )

@tarefas_bp.route('/adicionar', methods=['POST'])
@login_obrigatorio
def adicionar_tarefa():
    conteudo = request.form.get('tarefa')
    categoria_id = request.form.get('categoria_id')
    data_vencimento_str = request.form.get('data_vencimento')
    hora_criacao_str = request.form.get('hora_criacao')
    
    if conteudo:
        usuario_id = session.get('usuario_id')
        
        # Converter string de data para objeto date, se fornecida
        data_vencimento = None
        if data_vencimento_str and data_vencimento_str != '':
            try:
                data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use YYYY-MM-DD', 'erro')
                return redirect(url_for('tarefas.index'))
        
        # Definir a data e hora de criação - usar a hora especificada pelo usuário ou a atual
        data_criacao = datetime.now()
        if hora_criacao_str and hora_criacao_str != '':
            try:
                # Separar a hora e minuto da string HH:MM
                hora, minuto = map(int, hora_criacao_str.split(':'))
                # Criar um novo datetime com a data atual e a hora especificada
                data_criacao = datetime.now().replace(hour=hora, minute=minuto, second=0, microsecond=0)
            except ValueError:
                flash('Formato de hora inválido. Use HH:MM (24h)', 'erro')
                return redirect(url_for('tarefas.index'))
        
        # Obter notas (opcional)
        notas = request.form.get('notas')
        
        # Criar a tarefa com os dados fornecidos
        nova_tarefa = Tarefa(
            conteudo=conteudo, 
            usuario_id=usuario_id,
            data_vencimento=data_vencimento,
            data_criacao=data_criacao,  # Usar a data/hora definida
            notas=notas
        )
        
        if categoria_id and categoria_id != '':
            nova_tarefa.categoria_id = int(categoria_id)
            
        db.session.add(nova_tarefa)
        db.session.commit()
        
    return redirect(url_for('tarefas.index'))

@tarefas_bp.route('/marcar_concluida/<int:tarefa_id>', methods=['POST'])
@login_obrigatorio
def marcar_concluida(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    tarefa.concluida = not tarefa.concluida
    db.session.commit()
    return jsonify({'success': True, 'concluida': tarefa.concluida})

@tarefas_bp.route('/excluir/<int:tarefa_id>', methods=['POST'])
@login_obrigatorio
def excluir_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'success': True})

@tarefas_bp.route('/api/tarefas', methods=['GET'])
@login_obrigatorio
def api_tarefas():
    usuario_id = session.get('usuario_id')
    tarefas = Tarefa.query.filter_by(usuario_id=usuario_id).order_by(Tarefa.data_criacao).all()
    return jsonify([tarefa.to_dict() for tarefa in tarefas])

@tarefas_bp.route('/detalhes/<int:tarefa_id>')
@login_obrigatorio
def detalhes_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id).first_or_404()
    
    # Verificar se o usuário é o proprietário ou se a tarefa foi compartilhada com ele
    compartilhamento = None
    if tarefa.usuario_id != usuario_id:
        compartilhamento = TarefaCompartilhada.query.filter_by(
            tarefa_id=tarefa_id,
            usuario_compartilhado_id=usuario_id
        ).first_or_404()
    
    return render_template(
        'detalhes_tarefa.html',
        tarefa=tarefa,
        usuario_nome=session.get('usuario_nome'),
        compartilhamento=compartilhamento
    )

@tarefas_bp.route('/editar/<int:tarefa_id>', methods=['POST'])
@login_obrigatorio
def editar_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id).first_or_404()
    
    # Verificar permissões: usuário deve ser proprietário ou ter permissão de edição
    pode_editar = tarefa.usuario_id == usuario_id
    if not pode_editar:
        compartilhamento = TarefaCompartilhada.query.filter_by(
            tarefa_id=tarefa_id,
            usuario_compartilhado_id=usuario_id,
            permissao_edicao=True
        ).first()
        pode_editar = compartilhamento is not None
    
    if not pode_editar:
        flash('Você não tem permissão para editar esta tarefa', 'erro')
        return redirect(url_for('tarefas.index'))
    
    # Atualizar campos da tarefa
    tarefa.conteudo = request.form.get('conteudo', tarefa.conteudo)
    tarefa.notas = request.form.get('notas', tarefa.notas)
    
    data_vencimento_str = request.form.get('data_vencimento')
    if data_vencimento_str and data_vencimento_str != '':
        try:
            tarefa.data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'erro')
            return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
    else:
        tarefa.data_vencimento = None
    
    categoria_id = request.form.get('categoria_id')
    if categoria_id and categoria_id != '':
        tarefa.categoria_id = int(categoria_id)
    else:
        tarefa.categoria_id = None
    
    db.session.commit()
    flash('Tarefa atualizada com sucesso!', 'sucesso')
    return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
