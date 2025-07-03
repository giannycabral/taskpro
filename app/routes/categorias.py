"""
Blueprint de categorias
"""
from flask import Blueprint, redirect, url_for, request, flash, jsonify, session
from app import db
from app.models.categoria import Categoria
from app.models.tarefa import Tarefa
from app.utils.decorators import login_obrigatorio

# Criação do blueprint
categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/adicionar', methods=['POST'])
@login_obrigatorio
def adicionar_categoria():
    nome = request.form.get('nome_categoria')
    usuario_id = session.get('usuario_id')
    if nome:
        nova_categoria = Categoria(nome=nome, usuario_id=usuario_id)
        db.session.add(nova_categoria)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'sucesso')
    return redirect(url_for('tarefas.index'))

@categorias_bp.route('/excluir/<int:categoria_id>', methods=['POST'])
@login_obrigatorio
def excluir_categoria(categoria_id):
    usuario_id = session.get('usuario_id')
    categoria = Categoria.query.filter_by(id=categoria_id, usuario_id=usuario_id).first_or_404()
    
    # Remover a associação de tarefas com esta categoria
    Tarefa.query.filter_by(categoria_id=categoria_id).update({Tarefa.categoria_id: None})
    
    # Deletar a categoria
    db.session.delete(categoria)
    db.session.commit()
    
    flash('Categoria excluída com sucesso!', 'sucesso')
    return redirect(url_for('tarefas.index'))

@categorias_bp.route('/editar/<int:categoria_id>', methods=['POST'])
@login_obrigatorio
def editar_categoria(categoria_id):
    usuario_id = session.get('usuario_id')
    categoria = Categoria.query.filter_by(id=categoria_id, usuario_id=usuario_id).first_or_404()
    
    nome = request.form.get('nome_categoria')
    if nome:
        categoria.nome = nome
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'sucesso')
    
    return redirect(url_for('tarefas.index'))
