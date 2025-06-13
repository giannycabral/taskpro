# 📝 TaskPro - Sua Lista de Tarefas Eficiente

Um aplicativo web profissional e moderno para gerenciar suas tarefas diárias com eficiência.

## 📋 Visão Geral

TaskPro é uma aplicação web para gerenciamento de tarefas desenvolvida com Python/Flask no backend e HTML/CSS/JavaScript no frontend. A aplicação permite que usuários criem uma conta pessoal, adicionem tarefas, organizem por categorias, definam prazos e acompanhem seu progresso de forma eficiente.

## ✨ Funcionalidades

### Sistema de Usuários
- 👤 Registro e login de usuários
- 🔒 Proteção de rotas por autenticação
- 🔐 Senhas criptografadas com Werkzeug

### Gerenciamento de Tarefas
- ✅ Adicionar, editar e excluir tarefas
- ✓ Marcar tarefas como concluídas
- 📂 Organizar tarefas por categorias personalizadas
- 📅 Definir datas de vencimento para tarefas
- 🚨 Alertas visuais para tarefas próximas do vencimento ou vencidas

### Interface e Experiência do Usuário
- 🎨 Design profissional e moderno
- 📱 Layout totalmente responsivo
- 🔍 Filtros e busca de tarefas
- �� Ordenação por diversos critérios (data de criação, vencimento, alfabética)
- ⚡ Interações intuitivas via JavaScript

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-SQLAlchemy**: Integração do SQLAlchemy com Flask
- **SQLite**: Banco de dados
- **Werkzeug**: Utilitários, incluindo hashing de senhas

### Frontend
- **HTML5**
- **CSS3** (Design responsivo)
- **JavaScript** (Vanilla)
- **Google Fonts**

## 📦 Estrutura do Projeto

```
projeto-lista-de-tarefas/
│
├── app.py                 # Aplicação principal Flask
├── criar_bd.py            # Script para criação do banco de dados
├── requirements.txt       # Dependências do projeto
│
├── app/                   # Diretório da aplicação
│   ├── static/            # Arquivos estáticos
│   │   ├── css/           # Folhas de estilo
│   │   └── js/            # Scripts JavaScript
│   │
│   └── templates/         # Templates HTML
│
└── instance/              # Banco de dados SQLite (gerado automaticamente)
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

2. **Configure o ambiente**
```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados com usuário de teste
python criar_bd.py
```

3. **Execute a aplicação**
```bash
python app.py
```

4. **Acesse no navegador**: http://localhost:5001

### Usuário de Teste
- **Email**: teste@exemplo.com
- **Senha**: 123456

## 🔍 Exemplos de Uso

1. **Login ou Registro**
   - Acesse a página inicial para fazer login ou criar uma nova conta

2. **Adicionar uma Tarefa**
   - Digite o conteúdo da tarefa
   - Selecione uma categoria (ou deixe sem categoria)
   - Defina uma data de vencimento (opcional)
   - Clique em "Adicionar Tarefa"

3. **Gerenciar Categorias**
   - Crie novas categorias usando o formulário "Nova Categoria"
   - As tarefas serão organizadas por categoria automaticamente

4. **Filtrar e Ordenar**
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

## 🔮 Próximos Passos

Funcionalidades planejadas para futuras versões:
- Temas claro/escuro
- Sistema de notificações para tarefas próximas ao vencimento
- Compartilhamento de tarefas entre usuários
- Anexos e notas em tarefas
- Sincronização com calendários externos
- Aplicativo mobile

---

⌨️ com ❤️ por [REGIANE CABRAL](https://github.com/giannycabral)
