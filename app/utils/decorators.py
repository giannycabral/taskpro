"""
Decoradores utilizados no TaskPro
"""
from functools import wraps
from flask import session, redirect, url_for, flash

def login_obrigatorio(funcao):
    """
    Decorador que verifica se o usuário está logado.
    Redireciona para a página de login caso não esteja.
    """
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página', 'erro')
            return redirect(url_for('auth.login'))
        return funcao(*args, **kwargs)
    return wrapper
