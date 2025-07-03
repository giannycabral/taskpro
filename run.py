import os
from app import create_app

# Criar a aplicação utilizando a configuração padrão ou a definida na variável de ambiente
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, port=port, host='0.0.0.0')
