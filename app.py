from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Chave secreta para sessões
db = SQLAlchemy(app)

# Modelo de Categoria
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tarefas = db.relationship('Tarefa', backref='categoria', lazy=True)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    tarefas = db.relationship('Tarefa', backref='proprietario', lazy=True)
    categorias = db.relationship('Categoria', backref='usuario', lazy=True)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

# Modelo de Tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.Date, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)

    # Relacionamentos
    compartilhamentos = db.relationship('TarefaCompartilhada', foreign_keys=[TarefaCompartilhada.tarefa_id], backref='tarefa_origem', lazy=True)

    def __repr__(self):
        return f'<Tarefa {self.conteudo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'conteudo': self.conteudo,
            'concluida': self.concluida,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'data_vencimento': self.data_vencimento.strftime('%Y-%m-%d') if self.data_vencimento else None,
            'usuario_id': self.usuario_id,
            'categoria_id': self.categoria_id
        }
    
    @property
    def status_vencimento(self):
        """Retorna o status de vencimento da tarefa: 'normal', 'proximo' ou 'vencida'"""
        if not self.data_vencimento:
            return 'normal'
        
        hoje = date.today()
        dias_restantes = (self.data_vencimento - hoje).days
        
        if dias_restantes < 0:
            return 'vencida'
        elif dias_restantes <= 3:
            return 'proxima'
        else:
            return 'normal'

# Modelo de Compartilhamento de Tarefas
class TarefaCompartilhada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)
    proprietario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario_compartilhado_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_compartilhamento = db.Column(db.DateTime, default=datetime.utcnow)
    permissao_edicao = db.Column(db.Boolean, default=False)  # Define se o usuário pode editar a tarefa
    
    # Relacionamentos
    tarefa = db.relationship('Tarefa', foreign_keys=[tarefa_id], backref='compartilhamentos')
    proprietario = db.relationship('Usuario', foreign_keys=[proprietario_id], backref='tarefas_compartilhadas_por_mim')
    usuario_compartilhado = db.relationship('Usuario', foreign_keys=[usuario_compartilhado_id], backref='tarefas_compartilhadas_comigo')
    
    def __repr__(self):
        return f'<TarefaCompartilhada {self.tarefa_id} de {self.proprietario_id} para {self.usuario_compartilhado_id}>'

# Crie o banco de dados se não existir
with app.app_context():
    db.create_all()

# Função auxiliar para verificar se o usuário está logado
def login_obrigatorio(funcao):
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página', 'erro')
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)
    wrapper.__name__ = funcao.__name__
    return wrapper

# Rotas de autenticação
@app.route('/registro', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
        
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu com sucesso', 'sucesso')
    return redirect(url_for('login'))

# Rotas da aplicação
@app.route('/')
@login_obrigatorio
def index():
    usuario_id = session.get('usuario_id')
    categorias = Categoria.query.filter_by(usuario_id=usuario_id).all()
    
    # Obter parâmetros de filtro e ordenação
    filtro_status = request.args.get('status', 'todas')
    ordem = request.args.get('ordem', 'criacao')
    
    # Iniciar query básica
    query = Tarefa.query.filter_by(usuario_id=usuario_id)
    
    # Aplicar filtros de status
    if filtro_status == 'concluidas':
        query = query.filter_by(concluida=True)
    elif filtro_status == 'pendentes':
        query = query.filter_by(concluida=False)
    
    # Aplicar ordenação
    if ordem == 'vencimento':
        # Ordenar tarefas com vencimento primeiro, as sem vencimento depois
        query = query.order_by(
            (Tarefa.data_vencimento == None).asc(),  # Coloca NULL (sem data) por último
            Tarefa.data_vencimento.asc(),            # Ordena por data crescente
            Tarefa.data_criacao.desc()               # Se mesma data, mostra mais recente primeiro
        )
    elif ordem == 'vencimento_desc':
        # Ordenar por data de vencimento decrescente (mais distante primeiro)
        query = query.order_by(
            (Tarefa.data_vencimento == None).asc(),  # Coloca NULL (sem data) por último 
            Tarefa.data_vencimento.desc(),           # Ordena por data decrescente
            Tarefa.data_criacao.desc()               # Se mesma data, mostra mais recente primeiro
        )
    elif ordem == 'criacao_desc':
        # Mais antigas primeiro
        query = query.order_by(Tarefa.data_criacao.asc())
    else:  # criacao (padrão)
        # Mais recentes primeiro
        query = query.order_by(Tarefa.data_criacao.desc())
    
    # Executar a consulta
    tarefas = query.all()
    
    # O status de vencimento será calculado via propriedade status_vencimento
    # Não precisamos fazer nada aqui, pois a propriedade já calcula automaticamente
    
    # Agrupar tarefas por categoria
    tarefas_por_categoria = {}
    for categoria in categorias:
        tarefas_por_categoria[categoria.nome] = [t for t in tarefas if t.categoria_id == categoria.id]
    tarefas_sem_categoria = [t for t in tarefas if t.categoria_id is None]
    
    # Verificar quantas tarefas foram compartilhadas com o usuário
    contagem_compartilhadas = TarefaCompartilhada.query.filter_by(usuario_compartilhado_id=usuario_id).count()
    
    return render_template(
        'index.html',
        tarefas=tarefas,
        usuario_nome=session.get('usuario_nome'),
        categorias=categorias,
        tarefas_por_categoria=tarefas_por_categoria,
        contagem_compartilhadas=contagem_compartilhadas,
        tarefas_sem_categoria=tarefas_sem_categoria,
        filtro_status=filtro_status,
        ordem=ordem
    )

@app.route('/adicionar', methods=['POST'])
@login_obrigatorio
def adicionar_tarefa():
    conteudo = request.form.get('tarefa')
    categoria_id = request.form.get('categoria_id')
    data_vencimento_str = request.form.get('data_vencimento')
    
    if conteudo:
        usuario_id = session.get('usuario_id')
        
        # Converter string de data para objeto date, se fornecida
        data_vencimento = None
        if data_vencimento_str and data_vencimento_str != '':
            try:
                data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use YYYY-MM-DD', 'erro')
                return redirect(url_for('index'))
        
        # Criar a tarefa com os dados fornecidos
        nova_tarefa = Tarefa(
            conteudo=conteudo, 
            usuario_id=usuario_id,
            data_vencimento=data_vencimento
        )
        
        if categoria_id and categoria_id != '':
            nova_tarefa.categoria_id = int(categoria_id)
            
        db.session.add(nova_tarefa)
        db.session.commit()
        
    return redirect(url_for('index'))

@app.route('/adicionar_categoria', methods=['POST'])
@login_obrigatorio
def adicionar_categoria():
    nome = request.form.get('nome_categoria')
    usuario_id = session.get('usuario_id')
    if nome:
        nova_categoria = Categoria(nome=nome, usuario_id=usuario_id)
        db.session.add(nova_categoria)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/marcar_concluida/<int:tarefa_id>', methods=['POST'])
@login_obrigatorio
def marcar_concluida(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    tarefa.concluida = not tarefa.concluida
    db.session.commit()
    return jsonify({'success': True, 'concluida': tarefa.concluida})

@app.route('/excluir/<int:tarefa_id>', methods=['POST'])
@login_obrigatorio
def excluir_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'success': True})

# API para obter todas as tarefas em formato JSON
@app.route('/api/tarefas', methods=['GET'])
@login_obrigatorio
def api_tarefas():
    usuario_id = session.get('usuario_id')
    tarefas = Tarefa.query.filter_by(usuario_id=usuario_id).order_by(Tarefa.data_criacao).all()
    return jsonify([tarefa.to_dict() for tarefa in tarefas])

@app.route('/compartilhar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
@login_obrigatorio
def compartilhar_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first_or_404()
    
    if request.method == 'POST':
        # Recebe o email do usuário com quem compartilhar
        email_destinatario = request.form.get('email')
        permissao_edicao = 'permissao_edicao' in request.form
        
        # Verifica se o email foi fornecido
        if not email_destinatario:
            flash('Por favor, insira o email do usuário com quem deseja compartilhar a tarefa', 'erro')
            return redirect(url_for('compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se o usuário existe
        destinatario = Usuario.query.filter_by(email=email_destinatario).first()
        if not destinatario:
            flash('Usuário não encontrado', 'erro')
            return redirect(url_for('compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se não está tentando compartilhar consigo mesmo
        if destinatario.id == usuario_id:
            flash('Você não pode compartilhar uma tarefa consigo mesmo', 'erro')
            return redirect(url_for('compartilhar_tarefa', tarefa_id=tarefa_id))
            
        # Verifica se a tarefa já está compartilhada com esse usuário
        compartilhamento_existente = TarefaCompartilhada.query.filter_by(
            tarefa_id=tarefa_id,
            proprietario_id=usuario_id,
            usuario_compartilhado_id=destinatario.id
        ).first()
        
        if compartilhamento_existente:
            # Atualiza as permissões se já estiver compartilhada
            compartilhamento_existente.permissao_edicao = permissao_edicao
            db.session.commit()
            flash(f'Tarefa já compartilhada com {destinatario.nome}. Permissões atualizadas.', 'sucesso')
            return redirect(url_for('index'))
            
        # Cria um novo compartilhamento
        novo_compartilhamento = TarefaCompartilhada(
            tarefa_id=tarefa_id,
            proprietario_id=usuario_id,
            usuario_compartilhado_id=destinatario.id,
            permissao_edicao=permissao_edicao
        )
        
        db.session.add(novo_compartilhamento)
        db.session.commit()
        
        flash(f'Tarefa compartilhada com {destinatario.nome} com sucesso!', 'sucesso')
        return redirect(url_for('index'))
        
    # Carrega a lista de usuários para o formulário de compartilhamento (exclui o usuário atual)
    usuarios = Usuario.query.filter(Usuario.id != usuario_id).all()
    
    # Carrega os compartilhamentos existentes para esta tarefa
    compartilhamentos = TarefaCompartilhada.query.filter_by(
        tarefa_id=tarefa_id,
        proprietario_id=usuario_id
    ).all()
    
    compartilhamentos_info = []
    for c in compartilhamentos:
        compartilhamentos_info.append({
            'id': c.id,
            'nome_usuario': c.usuario_compartilhado.nome,
            'email_usuario': c.usuario_compartilhado.email,
            'permissao_edicao': c.permissao_edicao,
            'data': c.data_compartilhamento.strftime('%d/%m/%Y %H:%M')
        })
    
    return render_template(
        'compartilhar_tarefa.html',
        tarefa=tarefa,
        usuarios=usuarios,
        compartilhamentos=compartilhamentos_info
    )

@app.route('/remover_compartilhamento/<int:compartilhamento_id>', methods=['POST'])
@login_obrigatorio
def remover_compartilhamento(compartilhamento_id):
    usuario_id = session.get('usuario_id')
    
    # Busca o compartilhamento e verifica se o usuário atual é o proprietário
    compartilhamento = TarefaCompartilhada.query.filter_by(id=compartilhamento_id, proprietario_id=usuario_id).first_or_404()
    
    # Armazena o ID da tarefa para redirecionamento
    tarefa_id = compartilhamento.tarefa_id
    
    # Remove o compartilhamento
    db.session.delete(compartilhamento)
    db.session.commit()
    
    flash('Compartilhamento removido com sucesso', 'sucesso')
    return redirect(url_for('compartilhar_tarefa', tarefa_id=tarefa_id))

@app.route('/tarefas_compartilhadas')
@login_obrigatorio
def tarefas_compartilhadas():
    usuario_id = session.get('usuario_id')
    
    # Busca todas as tarefas compartilhadas com o usuário atual
    compartilhamentos = TarefaCompartilhada.query.filter_by(usuario_compartilhado_id=usuario_id).all()
    
    tarefas_compartilhadas = []
    for c in compartilhamentos:
        tarefa = c.tarefa
        proprietario = c.proprietario
        
        tarefas_compartilhadas.append({
            'tarefa': tarefa,
            'proprietario': proprietario,
            'data_compartilhamento': c.data_compartilhamento,
            'permissao_edicao': c.permissao_edicao,
            'compartilhamento_id': c.id
        })
    
    return render_template(
        'tarefas_compartilhadas.html',
        tarefas_compartilhadas=tarefas_compartilhadas
    )

@app.route('/editar_tarefa_compartilhada/<int:compartilhamento_id>', methods=['GET', 'POST'])
@login_obrigatorio
def editar_tarefa_compartilhada(compartilhamento_id):
    usuario_id = session.get('usuario_id')
    
    # Busca o compartilhamento e verifica se o usuário tem permissão
    compartilhamento = TarefaCompartilhada.query.filter_by(
        id=compartilhamento_id, 
        usuario_compartilhado_id=usuario_id,
        permissao_edicao=True
    ).first_or_404()
    
    tarefa = compartilhamento.tarefa
    
    if request.method == 'POST':
        conteudo = request.form.get('tarefa')
        data_vencimento_str = request.form.get('data_vencimento')
        
        if conteudo:
            tarefa.conteudo = conteudo
            
            # Atualiza a data de vencimento, se fornecida
            data_vencimento = None
            if data_vencimento_str and data_vencimento_str != '':
                try:
                    data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
                    tarefa.data_vencimento = data_vencimento
                except ValueError:
                    flash('Formato de data inválido. Use YYYY-MM-DD', 'erro')
                    return redirect(url_for('editar_tarefa_compartilhada', compartilhamento_id=compartilhamento_id))
            
            db.session.commit()
            flash('Tarefa compartilhada atualizada com sucesso!', 'sucesso')
            return redirect(url_for('tarefas_compartilhadas'))
    
    return render_template('editar_tarefa_compartilhada.html', tarefa=tarefa, compartilhamento=compartilhamento)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
