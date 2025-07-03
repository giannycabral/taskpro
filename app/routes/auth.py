"""
Blueprint de autenticação
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Usuario
from app.utils.decorators import login_obrigatorio

# Criação do blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validação dos campos
        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios', 'erro')
            return render_template('registro.html')
            
        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'erro')
            return render_template('registro.html')
            
        # Verificar se o email já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este email já está registrado', 'erro')
            return render_template('registro.html')
        
        # Criar novo usuário
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Registro realizado com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('auth.login'))
        
    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario or not usuario.verificar_senha(senha):
            flash('Email ou senha incorretos', 'erro')
            return render_template('login.html')
            
        # Criar sessão de usuário
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        
        flash(f'Bem-vindo de volta, {usuario.nome}!', 'sucesso')
        return redirect(url_for('tarefas.index'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu com sucesso', 'sucesso')
    return redirect(url_for('auth.login'))
