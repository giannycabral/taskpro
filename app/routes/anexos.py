"""
Blueprint de anexos
"""
from flask import Blueprint, redirect, url_for, request, flash, send_from_directory, session, current_app
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app import db
from app.models.tarefa import Tarefa
from app.models.anexo import Anexo
from app.models.compartilhamento import TarefaCompartilhada
from app.utils.decorators import login_obrigatorio

# Criação do blueprint
anexos_bp = Blueprint('anexos', __name__, url_prefix='/anexos')

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@anexos_bp.route('/tarefa/<int:tarefa_id>/adicionar', methods=['POST'])
@login_obrigatorio
def adicionar_anexo(tarefa_id):
    """Adiciona um anexo a uma tarefa."""
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id).first_or_404()
    
    # Verificar permissões
    if tarefa.usuario_id != usuario_id:
        compartilhamento = TarefaCompartilhada.query.filter_by(
            tarefa_id=tarefa_id, 
            usuario_compartilhado_id=usuario_id,
            permissao_edicao=True
        ).first()
        
        if not compartilhamento:
            flash('Você não tem permissão para adicionar anexos a esta tarefa', 'erro')
            return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
    
    # Verificar se o arquivo foi enviado
    if 'arquivo' not in request.files:
        flash('Nenhum arquivo selecionado', 'erro')
        return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
    
    arquivo = request.files['arquivo']
    
    # Se o usuário não selecionar um arquivo
    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado', 'erro')
        return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
    
    # Se o arquivo é válido e permitido
    if arquivo and allowed_file(arquivo.filename):
        # Garantir nome de arquivo seguro
        filename = secure_filename(arquivo.filename)
        
        # Criar pasta específica para a tarefa, se não existir
        tarefa_upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], f'tarefa_{tarefa_id}')
        os.makedirs(tarefa_upload_dir, exist_ok=True)
        
        # Acrescentar timestamp ao nome do arquivo para evitar duplicatas
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename_with_timestamp = f"{timestamp}_{filename}"
        
        # Caminho completo para salvar o arquivo
        filepath = os.path.join(tarefa_upload_dir, filename_with_timestamp)
        
        # Salvar o arquivo
        arquivo.save(filepath)
        
        # Criar registro no banco de dados
        novo_anexo = Anexo(
            nome_arquivo=filename,
            caminho_arquivo=os.path.join(f'tarefa_{tarefa_id}', filename_with_timestamp),
            tipo_arquivo=arquivo.content_type,
            tamanho=os.path.getsize(filepath),
            tarefa_id=tarefa_id,
            usuario_id=usuario_id
        )
        
        db.session.add(novo_anexo)
        db.session.commit()
        
        flash('Arquivo anexado com sucesso', 'sucesso')
    else:
        flash(f'Tipo de arquivo não permitido. Formatos aceitos: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'erro')
    
    return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))

@anexos_bp.route('/<int:anexo_id>/download')
@login_obrigatorio
def download_anexo(anexo_id):
    """Faz o download de um anexo."""
    usuario_id = session.get('usuario_id')
    
    # Obter o anexo
    anexo = Anexo.query.filter_by(id=anexo_id).first_or_404()
    
    # Verificar a permissão (usuário dono da tarefa ou com tarefa compartilhada)
    tarefa = Tarefa.query.filter_by(id=anexo.tarefa_id).first()
    
    if tarefa.usuario_id != usuario_id:
        compartilhamento = TarefaCompartilhada.query.filter_by(
            tarefa_id=anexo.tarefa_id, 
            usuario_compartilhado_id=usuario_id
        ).first()
        
        if not compartilhamento:
            flash('Você não tem permissão para baixar este anexo', 'erro')
            return redirect(url_for('tarefas.index'))
    
    try:
        return send_from_directory(
            directory=current_app.config['UPLOAD_FOLDER'], 
            path=anexo.caminho_arquivo, 
            as_attachment=True,
            download_name=anexo.nome_arquivo
        )
    except FileNotFoundError:
        flash('Arquivo não encontrado', 'erro')
        return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=anexo.tarefa_id))

@anexos_bp.route('/<int:anexo_id>/excluir', methods=['POST'])
@login_obrigatorio
def excluir_anexo(anexo_id):
    """Exclui um anexo da tarefa."""
    usuario_id = session.get('usuario_id')
    
    # Obter o anexo
    anexo = Anexo.query.filter_by(id=anexo_id).first_or_404()
    tarefa_id = anexo.tarefa_id
    
    # Verificar permissão (apenas o proprietário da tarefa ou do anexo pode excluir)
    tarefa = Tarefa.query.filter_by(id=tarefa_id).first()
    
    if tarefa.usuario_id != usuario_id and anexo.usuario_id != usuario_id:
        flash('Você não tem permissão para excluir este anexo', 'erro')
        return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
    
    # Excluir o arquivo físico
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], anexo.caminho_arquivo)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Erro ao excluir arquivo: {str(e)}")
    
    # Excluir registro do anexo do banco de dados
    db.session.delete(anexo)
    db.session.commit()
    
    flash('Anexo excluído com sucesso', 'sucesso')
    return redirect(url_for('tarefas.detalhes_tarefa', tarefa_id=tarefa_id))
