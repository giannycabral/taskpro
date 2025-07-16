# 📝 TaskPro - Sua Lista de Tarefas Eficiente

Um aplicativo web profissional e moderno para gerenciar suas tarefas diárias com eficiência.

[![Demo TaskPro](https://img.shields.io/badge/Demo-GitHub%20Pages-brightgreen)](https://giannycabral.github.io/taskpro/)

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
├── app.py.old             # Arquivo legado (será removido na próxima fase)
├── config.py              # Configurações da aplicação
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

## 🌐 Versão Online

Uma versão demonstrativa do TaskPro está disponível através do GitHub Pages:

**[Acessar Demo do TaskPro](https://giannycabral.github.io/taskpro/)**

Note que esta é uma versão estática para demonstração visual. Para ter acesso a todas as funcionalidades, siga as instruções de instalação abaixo.

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
python scripts/criar_bd.py
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

## 📁 Sistema de Uploads e Anexos

O TaskPro possui um sistema completo para gerenciar anexos de arquivos nas tarefas:

### Diretório de Uploads
- O diretório `app/uploads/` armazena todos os arquivos anexados às tarefas
- Este diretório é criado automaticamente quando a aplicação é iniciada pela primeira vez
- Os arquivos são organizados de forma segura e mantêm seus nomes originais
- O sistema aceita diversos tipos de arquivos: documentos, imagens, PDFs, planilhas, apresentações e arquivos zip

### Tipos de arquivos permitidos
- Documentos: `.txt`, `.doc`, `.docx`
- Imagens: `.png`, `.jpg`, `.jpeg`, `.gif`
- PDFs: `.pdf`
- Planilhas: `.xls`, `.xlsx`
- Apresentações: `.ppt`, `.pptx`
- Arquivos compactados: `.zip`

### Limites e segurança
- O tamanho máximo de arquivo é de 16MB para evitar sobrecarga do servidor
- O sistema implementa validações de segurança para evitar uploads maliciosos
- Os anexos são vinculados à tarefa e ao usuário, garantindo que apenas pessoas autorizadas possam acessá-los

### Como funciona
1. Ao adicionar uma tarefa ou editar seus detalhes, o usuário pode anexar arquivos
2. Os arquivos são automaticamente processados, validados e armazenados no servidor
3. Os anexos podem ser visualizados, baixados ou excluídos na página de detalhes da tarefa
4. Quando uma tarefa é excluída, seus anexos são automaticamente removidos do sistema

## 🤝 Contribuição

Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga estes passos:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

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
