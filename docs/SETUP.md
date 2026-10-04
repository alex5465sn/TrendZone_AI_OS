# Setup Local - TrendZone AI OS

## 📋 Pré-requisitos

- **Python 3.10+** (recomendado 3.11)
- **Node.js 18+** (recomendado 20)
- **Docker & Docker Compose** (opcional, para containerização)
- **Git**
- **VS Code** (recomendado)

---

## 🚀 Setup Rápido (Docker)

### 1. Clone o repositório

```bash
git clone https://github.com/alex5465sn/TrendZone_AI_OS.git
cd TrendZone_AI_OS
```

### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Inicie com Docker Compose

```bash
docker-compose up -d
```

### 4. Acesse a aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

---

## 🛠️ Setup Manual (Desenvolvimento)

### Backend

#### 1. Crie um ambiente virtual Python

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### 2. Instale dependências

```bash
pip install -r requirements.txt
```

#### 3. Configure variáveis de ambiente

```bash
cp .env.example ../.env
# Edite ../.env com suas credenciais
```

#### 4. Inicialize o banco de dados

```bash
python -c "from app.database import init_db; init_db()"
```

#### 5. Inicie o servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: **http://localhost:8000**

Documentação interativa: **http://localhost:8000/docs**

### Frontend

#### 1. Instale dependências

```bash
cd frontend
npm install
```

#### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
# Edite .env se necessário
```

#### 3. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em: **http://localhost:5173**

---

## 🔧 Variáveis de Ambiente

### Backend (`.env`)

```env
# APP
APP_NAME=TrendZone AI OS
VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# DATABASE
DATABASE_URL=sqlite:///trendzone.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# SHOPEE
SHOPEE_GRAPHQL_URL=https://open-api.affiliate.shopee.com.br/graphql
SHOPEE_APP_ID=your-app-id
SHOPEE_SECRET=your-secret

# MERCADO LIVRE
MERCADOLIVRE_CLIENT_ID=your-client-id
MERCADOLIVRE_CLIENT_SECRET=your-client-secret
MERCADOLIVRE_REDIRECT_URI=http://localhost:5173/accounts/ml-callback

# FACEBOOK
FACEBOOK_APP_ID=your-app-id
FACEBOOK_APP_SECRET=your-secret
FACEBOOK_PAGE_ID=your-page-id
FACEBOOK_PAGE_TOKEN=your-token

# ABACUS AI
ABACUS_API_KEY=your-api-key

# OPENROUTER
OPENROUTER_API_KEY=your-api-key

# REDIS (opcional)
REDIS_URL=redis://localhost:6379

# RABBITMQ (opcional)
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### Frontend (`.env`)

```env
VITE_API_URL=http://localhost:8000
```

---

## 📦 Estrutura de Pastas

```
TrendZone_AI_OS/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # Endpoints
│   │   ├── services/          # Lógica de negócio
│   │   ├── models/            # ORM
│   │   ├── schemas/           # Validação
│   │   ├── repositories/      # Data access
│   │   ├── integrations/      # APIs externas
│   │   ├── agents/            # IA Agents
│   │   ├── tasks/             # Background jobs
│   │   ├── core/              # Configurações
│   │   ├── database/          # Setup DB
│   │   └── main.py            # Entry point
│   ├── tests/                 # Testes
│   ├── requirements.txt        # Dependências
│   └── Dockerfile
│
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── pages/             # Páginas
│   │   ├── components/        # Componentes
│   │   ├── services/          # API clients
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   ├── utils/             # Utilitários
│   │   ├── routes/            # Rotas
│   │   └── App.tsx
│   ├── tests/                 # Testes
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docs/                       # Documentação
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── DEPLOYMENT.md
│   └── specs/
│
├── scripts/                    # Scripts utilitários
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
│
├── docker-compose.yml          # Orquestração Docker
├── .env.example                # Template de .env
├── README.md
└── .gitignore
```

---

## 🧪 Testes

### Backend

```bash
cd backend

# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=app tests/

# Rodar teste específico
pytest tests/test_auth.py
```

### Frontend

```bash
cd frontend

# Rodar testes
npm run test

# Rodar com cobertura
npm run test:coverage

# Modo watch
npm run test:watch
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'app'"

**Solução**: Certifique-se de estar no diretório `backend/` e que o ambiente virtual está ativado.

```bash
cd backend
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
```

### Erro: "Port 8000 already in use"

**Solução**: Mude a porta ou mate o processo usando a porta 8000.

```bash
# Usar porta diferente
uvicorn app.main:app --reload --port 8001

# Ou matar processo (Linux/macOS)
lsof -ti:8000 | xargs kill -9
```

### Erro: "Cannot find module 'react'"

**Solução**: Instale as dependências do frontend.

```bash
cd frontend
npm install
```

### Erro: "Database is locked"

**Solução**: SQLite tem limitações com concorrência. Para produção, use PostgreSQL.

```bash
# Remova o arquivo de banco de dados
rm backend/trendzone.db

# Reinicialize
python -c "from app.database import init_db; init_db()"
```

---

## 📚 Próximos Passos

1. ✅ Setup local concluído
2. ⏭️ Leia [ARCHITECTURE.md](./ARCHITECTURE.md) para entender a estrutura
3. ⏭️ Explore os endpoints em http://localhost:8000/docs
4. ⏭️ Crie um usuário de teste
5. ⏭️ Teste as integrações (Shopee, Mercado Livre, etc)

---

## 🤝 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m "feat: descrição"`
3. Push para a branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub ou entre em contato com o time de desenvolvimento.
