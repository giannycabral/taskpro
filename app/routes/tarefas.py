"""
Blueprint de tarefas
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

# Criação do blueprint
tarefas_bp = Blueprint('tarefas', __name__)

# As rotas serão implementadas aqui posteriormente
