#!/bin/bash

echo "Iniciando a aplicação TaskPro..."
cd /workspaces/projeto-lista-de-tarefas
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
