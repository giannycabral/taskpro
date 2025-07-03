"""
Blueprint de anexos
"""
from flask import Blueprint, redirect, url_for, request, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

# Criação do blueprint
anexos_bp = Blueprint('anexos', __name__)

# As rotas serão implementadas aqui posteriormente
