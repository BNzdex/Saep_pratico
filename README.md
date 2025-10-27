# Sistema SAEP - Gestão de Estoque

Sistema web desenvolvido em Python Flask para gerenciamento de produtos e controle de estoque.

## Funcionalidades

- ✅ Autenticação de usuários (login/logout)
- ✅ Dashboard principal
- ✅ Cadastro de produtos (CRUD completo)
- ✅ Busca de produtos
- ✅ Gestão de estoque (entrada/saída)
- ✅ Alertas de estoque mínimo
- ✅ Ordenação alfabética de produtos (Bubble Sort)
- ✅ Banco de dados SQLite com dados pré-cadastrados

## Requisitos

- Python 3.8+
- Flask 3.0.0

## Instalação

1. Clone ou baixe o projeto

2. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Inicialize o banco de dados:
\`\`\`bash
python init_db.py
\`\`\`

4. Execute a aplicação:
\`\`\`bash
python app.py
\`\`\`

5. Acesse no navegador:
\`\`\`
http://localhost:5000
\`\`\`

## Usuários de Teste

- **Admin**: username: `admin` | senha: `admin123`
- **João**: username: `joao` | senha: `senha123`
- **Maria**: username: `maria` | senha: `senha456`

## Estrutura do Banco de Dados

### Tabela: usuarios
- id (INTEGER, PRIMARY KEY)
- username (TEXT, UNIQUE)
- password (TEXT)
- nome (TEXT)
- email (TEXT)

### Tabela: produtos
- id (INTEGER, PRIMARY KEY)
- nome (TEXT)
- descricao (TEXT)
- preco (REAL)
- quantidade (INTEGER)
- estoque_minimo (INTEGER)

### Tabela: movimentacoes
- id (INTEGER, PRIMARY KEY)
- produto_id (INTEGER, FOREIGN KEY)
- tipo (TEXT: 'entrada' ou 'saida')
- quantidade (INTEGER)
- data_movimentacao (DATE)

## Estrutura do Projeto

\`\`\`
saep-flask-system/
├── app.py                  # Aplicação Flask principal
├── init_db.py             # Script de inicialização do banco
├── requirements.txt       # Dependências Python
├── saep_db.db            # Banco de dados SQLite (gerado)
├── static/
│   └── css/
│       └── style.css     # Estilos CSS
└── templates/
    ├── login.html        # Página de login
    ├── dashboard.html    # Dashboard principal
    ├── produtos.html     # Gestão de produtos
    └── estoque.html      # Gestão de estoque
\`\`\`

## Funcionalidades Detalhadas

### Autenticação
- Login com validação de credenciais
- Mensagens de erro personalizadas
- Proteção de rotas com decorator `@login_required`
- Sessão de usuário com informações do perfil

### Cadastro de Produtos
- Listagem completa de produtos
- Busca por nome ou descrição
- Adicionar novo produto com validações
- Editar produto existente
- Excluir produto com confirmação
- Validações de campos obrigatórios e valores numéricos

### Gestão de Estoque
- Listagem ordenada alfabeticamente (Bubble Sort)
- Registro de movimentações (entrada/saída)
- Validação de quantidade disponível
- Alerta automático quando estoque fica abaixo do mínimo
- Indicadores visuais de status do estoque
- Histórico de movimentações no banco de dados

## Tecnologias Utilizadas

- **Backend**: Python 3 + Flask
- **Banco de Dados**: SQLite3
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Algoritmo de Ordenação**: Bubble Sort
