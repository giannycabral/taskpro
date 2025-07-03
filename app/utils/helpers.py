"""
Funções auxiliares do TaskPro
"""
from flask import current_app

def allowed_file(filename):
    """
    Verifica se a extensão de um arquivo é permitida.
    
    Args:
        filename (str): Nome do arquivo a ser verificado
        
    Returns:
        bool: True se a extensão for permitida, False caso contrário
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
