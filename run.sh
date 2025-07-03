#!/bin/bash

echo "Iniciando a aplicação TaskPro..."
cd /workspaces/taskpro
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
