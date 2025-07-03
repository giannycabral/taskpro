#!/bin/bash

echo "Iniciando a aplicação TaskPro..."
cd /workspaces/taskpro
export FLASK_APP=run.py
export FLASK_ENV=development
python run.py
