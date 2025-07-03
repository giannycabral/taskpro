# 📝 TaskPro - Sua Lista de Tarefas Eficiente

Um aplicativo web profissional e moderno para gerenciar suas tarefas diárias com eficiência.

## 📋 Visão Geral

TaskPro é uma aplicação web para gerenciamento de tarefas desenvolvida com Python/Flask no backend e HTML/CSS/JavaScript no frontend. A aplicação permite que usuários criem uma conta pessoal, adicionem tarefas, organizem por categorias, definam prazos e acompanhem seu progresso de forma eficiente.

https://github.com/user-attachments/assets/538f6cc1-e12b-4054-bd5d-330cdc131e9c

## ✨ Funcionalidades

### Sistema de Usuários
- 👤 Registro e login de usuários
- 🔒 Proteção de rotas por autenticação
- 🔐 Senhas criptografadas com Werkzeug
- 👥 Compartilhamento de tarefas com outros usuários

### Gerenciamento de Tarefas
- ✅ Adicionar, editar e excluir tarefas
- ✓ Marcar tarefas como concluídas
- 📂 Organizar tarefas por categorias personalizadas
- 📅 Definir datas de vencimento para tarefas
- ⏰ Definir horários personalizados para tarefas
- 🚨 Alertas visuais para tarefas próximas do vencimento ou vencidas
- 📋 Adicionar notas detalhadas às tarefas
- 📎 Anexar arquivos às tarefas (PDF, documentos, imagens, etc.)
- 🔔 Sistema de notificações para tarefas próximas ao vencimento

### Interface e Experiência do Usuário
- 🎨 Design profissional e moderno com paleta lilás/rosa
- 📱 Layout totalmente responsivo
- 🔍 Filtros e busca de tarefas
- 📊 Ordenação por diversos critérios (data de criação, vencimento, alfabética)
- ⚡ Interações intuitivas via JavaScript
- 📝 Editor de notas aprimorado com contador de caracteres

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-SQLAlchemy**: Integração do SQLAlchemy com Flask
- **SQLite**: Banco de dados
- **Werkzeug**: Utilitários, incluindo hashing de senhas e manipulação de uploads

### Frontend
- **HTML5**
- **CSS3** (Design responsivo, animações e transições)
- **JavaScript** (Vanilla) com recursos modernos
- **Google Fonts**
- **Ícones e elementos visuais personalizados**

## 📦 Estrutura do Projeto (Refatorada)

```
taskpro/
│
├── app.py                 # Arquivo legado (será removido na próxima fase)
├── config.py              # Configurações da aplicação
├── criar_bd.py            # Script para criação do banco de dados
├── run.py                 # Script para executar a aplicação
├── run.sh                 # Script para execução fácil da aplicação
├── requirements.txt       # Dependências do projeto
│
├── app/                   # Diretório principal da aplicação
│   ├── __init__.py        # Inicialização da aplicação e registro de blueprints
│   │
│   ├── models/            # Modelos de dados
│   │   ├── __init__.py    # Importações dos modelos
│   │   ├── usuario.py     # Modelo de usuário
│   │   ├── tarefa.py      # Modelo de tarefa
│   │   ├── categoria.py   # Modelo de categoria
│   │   ├── compartilhamento.py  # Modelo de compartilhamento
│   │   ├── notificacao.py # Modelo de notificação
│   │   └── anexo.py       # Modelo de anexo
│   │
│   ├── routes/            # Rotas da aplicação
│   │   ├── __init__.py    # Importações dos blueprints
│   │   ├── auth.py        # Rotas de autenticação
│   │   ├── tarefas.py     # Rotas de tarefas
│   │   ├── categorias.py  # Rotas de categorias
│   │   ├── compartilhamento.py  # Rotas de compartilhamento
│   │   ├── notificacoes.py # Rotas de notificações
│   │   └── anexos.py      # Rotas de anexos
│   │
│   ├── static/            # Arquivos estáticos
│   │   ├── css/           # Folhas de estilo modulares
│   │   │   ├── taskpro_main.css           # Estilos principais
│   │   │   ├── taskpro_icons.css          # Ícones personalizados
│   │   │   ├── taskpro_attachments.css    # Estilos para anexos
│   │   │   ├── taskpro_form_notes.css     # Campos de notas
│   │   │   ├── taskpro_notes_improved.css # Editor aprimorado de notas
│   │   │   └── taskpro_share.css          # Estilos para compartilhamento
│   │   │
│   │   └── js/            # Scripts JavaScript
│   │       └── taskpro.js  # Funcionalidades interativas
│   │
│   ├── templates/         # Templates HTML
│   │   ├── index.html             # Página principal
│   │   ├── login.html            # Login de usuários
│   │   ├── registro.html         # Cadastro de usuários
│   │   ├── detalhes_tarefa.html  # Detalhes de tarefas
│   │   ├── notificacoes.html     # Página de notificações
│   │   ├── compartilhar_tarefa.html # Compartilhamento de tarefas
│   │   └── tarefas_compartilhadas.html # Tarefas compartilhadas
│   │
│   ├── uploads/           # Diretório para arquivos anexados às tarefas
│   │
│   └── utils/             # Utilitários
│       ├── __init__.py    # Inicialização de utilitários
│       ├── decorators.py  # Decoradores personalizados
│       └── helpers.py     # Funções auxiliares
│
├── instance/              # Banco de dados SQLite (gerado automaticamente)
│
└── scripts/               # Scripts auxiliares
    ├── __init__.py        # Inicialização de scripts
    └── criar_bd.py        # Script refatorado para criação do banco de dados
```

## 🚀 Como Usar

### Requisitos Prévios
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/taskpro
cd taskpro
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Crie o banco de dados**
```bash
python criar_bd.py
```

4. **Execute a aplicação**
```bash
python run.py
```
Ou você pode usar o script de execução:
```bash
chmod +x run.sh
./run.sh
```

5. **Acesse a aplicação**
Abra o navegador e acesse: `http://localhost:5005` ou `http://127.0.0.1:5005`

### Credenciais de Teste
Para fazer login com o usuário de teste criado automaticamente:
- **Email**: teste@exemplo.com
- **Senha**: 123456

## 🔍 Exemplos de Uso

1. **Login ou Registro**
   - Acesse a página inicial para fazer login ou criar uma nova conta

2. **Adicionar uma Tarefa**
   - Digite o conteúdo da tarefa
   - Selecione uma categoria (ou deixe sem categoria)
   - Defina uma data de vencimento (opcional)
   - Defina um horário específico (opcional)
   - Adicione notas detalhadas sobre a tarefa (opcional)
   - Anexe arquivos relevantes (opcional)
   - Clique em "Adicionar Tarefa"

3. **Gerenciar Anexos**
   - Na página de detalhes da tarefa, visualize e gerencie documentos anexados
   - Faça upload de novos arquivos
   - Baixe ou remova anexos existentes

4. **Compartilhar Tarefas**
   - Na página de detalhes da tarefa, clique em "Compartilhar"
   - Digite o email do usuário com quem deseja compartilhar
   - Defina se o usuário terá permissão para editar a tarefa
   - Visualize todas as tarefas compartilhadas com você no painel de tarefas compartilhadas

5. **Gerenciar Categorias**
   - Crie novas categorias usando o formulário "Nova Categoria"
   - As tarefas serão organizadas por categoria automaticamente

6. **Visualizar Notificações**
   - Clique no ícone de sino para ver suas notificações
   - Receba alertas sobre tarefas próximas do vencimento ou vencidas

7. **Filtrar e Ordenar**
   - Use os controles de filtro para ver apenas tarefas concluídas ou pendentes
   - Ordene tarefas por data de criação ou vencimento

## 🤝 Contribuição

Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga estes passos:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## 📅 Cronograma de Refatoração (✅ CONCLUÍDO)

A refatoração da estrutura do projeto foi concluída com sucesso, seguindo o cronograma abaixo:

1. **Dia 1**: ✅ Configuração da estrutura de diretórios e criação de arquivos base
   - Criada nova estrutura de pastas (app/models, app/routes, app/utils, etc.)
   - Configurados arquivos de inicialização (app/__init__.py, config.py, run.py)
   - Preparados módulos base e configurações iniciais

2. **Dia 2-3**: ✅ Refatoração dos modelos
   - Separado cada modelo em seu próprio arquivo (Usuario, Tarefa, Categoria, etc.)
   - Reorganizados relacionamentos entre modelos
   - Configuradas importações corretas e relacionamentos

3. **Dia 4-6**: ✅ Refatoração das rotas e implementação dos blueprints
   - Separadas rotas por funcionalidade (auth, tarefas, categorias, etc.)
   - Implementado sistema de blueprints
   - Ajustados redirecionamentos entre rotas

4. **Dia 7**: ✅ Ajuste de referências e imports entre arquivos
   - Corrigidas dependências circulares nos modelos (usando strings para referenciar relacionamentos)
   - Otimizados imports (agrupados por tipo e relevância)
   - Adicionada melhor documentação com docstrings
   - Refatorado o registro de blueprints usando lista centralizada
   - Implementada melhor organização de imports nas rotas e modelos

5. **Dia 8-9**: ✅ Testes e correção de bugs
   - Testados componentes individuais
   - Testados fluxos completos da aplicação
   - Corrigidos problemas identificados

6. **Dia 10**: ✅ Validação final e limpeza de código
   - Verificado funcionamento completo da aplicação
   - Removido código obsoleto
   - Documentada a nova estrutura

## 🔮 Próximos Passos

Funcionalidades planejadas para futuras versões:
- 🌓 Temas claro/escuro personalizáveis
- 📱 Versão mobile como Progressive Web App (PWA)
- 🔄 Sincronização com calendários externos (Google Calendar, Outlook)
- 📊 Dashboard com estatísticas e análise de produtividade
- 📥 Importação/exportação de tarefas em diversos formatos
- 🔄 Integração com outros serviços (Trello, Asana, etc.)
- 🌐 Suporte a múltiplos idiomas

---

⌨️ com ❤️ por [REGIANE CABRAL](https://github.com/giannycabral)
