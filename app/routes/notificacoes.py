"""
Blueprint de notificações
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app import db
from app.models.notificacao import Notificacao
from app.utils.decorators import login_obrigatorio

# Criação do blueprint
notificacoes_bp = Blueprint('notificacoes', __name__, url_prefix='/notificacoes')

@notificacoes_bp.route('/')
@login_obrigatorio
def index():
    usuario_id = session.get('usuario_id')
    
    # Busca todas as notificações do usuário ordenadas por data (mais recentes primeiro)
    notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id).order_by(Notificacao.data_criacao.desc()).all()
    
    # Conta quantas notificações não foram lidas
    notificacoes_nao_lidas = Notificacao.query.filter_by(usuario_id=usuario_id, lida=False).count()
    
    return render_template(
        'notificacoes.html',
        notificacoes=notificacoes,
        notificacoes_nao_lidas=notificacoes_nao_lidas
    )

@notificacoes_bp.route('/marcar_lida/<int:notificacao_id>', methods=['POST'])
@login_obrigatorio
def marcar_notificacao_lida(notificacao_id):
    usuario_id = session.get('usuario_id')
    
    # Busca a notificação e verifica se pertence ao usuário
    notificacao = Notificacao.query.filter_by(id=notificacao_id, usuario_id=usuario_id).first_or_404()
    
    # Marca como lida
    notificacao.lida = True
    db.session.commit()
    
    return jsonify({'success': True})

@notificacoes_bp.route('/marcar_todas_lidas', methods=['POST'])
@login_obrigatorio
def marcar_todas_notificacoes_lidas():
    usuario_id = session.get('usuario_id')
    
    # Busca todas as notificações não lidas
    notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id, lida=False).all()
    
    # Marca todas como lidas
    for notificacao in notificacoes:
        notificacao.lida = True
    
    db.session.commit()
    
    return jsonify({'success': True})

@notificacoes_bp.route('/excluir/<int:notificacao_id>', methods=['POST'])
@login_obrigatorio
def excluir_notificacao(notificacao_id):
    usuario_id = session.get('usuario_id')
    
    # Busca a notificação e verifica se pertence ao usuário
    notificacao = Notificacao.query.filter_by(id=notificacao_id, usuario_id=usuario_id).first_or_404()
    
    # Exclui a notificação
    db.session.delete(notificacao)
    db.session.commit()
    
    return jsonify({'success': True})
