# Arquitetura TrendZone AI OS

## 📋 Visão Geral

TrendZone AI OS é um sistema operacional de IA para gerenciamento de afiliados em marketplaces. Combina análise inteligente de produtos, automação de publicações e integração com múltiplos canais de venda.

### Stack Tecnológico

- **Backend**: FastAPI + SQLAlchemy + Python 3.11
- **Frontend**: React 18 + TypeScript + Vite
- **Banco de Dados**: SQLite (dev) / PostgreSQL (prod)
- **Containerização**: Docker + Docker Compose
- **Integrações**: Shopee, Mercado Livre, Facebook, WhatsApp, Abacus AI

---

## 🏗️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              (pages, components, services)               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│                  API Layer (FastAPI)                     │
│         (rotas, validação, autenticação)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               Service Layer                              │
│      (lógica de negócio, orquestração)                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            Repository Layer                              │
│         (acesso a dados, queries)                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Model Layer (SQLAlchemy)                    │
│           (ORM, schemas, validação)                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            Database (SQLite/PostgreSQL)                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios

### Backend (`backend/app/`)

```
app/
├── api/                          # Endpoints REST
│   ├── auth.py                  # Autenticação
│   ├── marketplace.py           # Marketplaces genéricos
│   ├── mercadolivre.py          # Mercado Livre específico
│   ├── products.py              # Produtos
│   ├── dashboard.py             # Dashboard
│   └── ...
│
├── services/                     # Lógica de negócio
│   ├── marketplace_account_service.py
│   ├── mercadolivre_auth_service.py
│   ├── product_service.py
│   ├── scout_service.py
│   └── ...
│
├── models/                       # SQLAlchemy ORM
│   ├── user.py
│   ├── product.py
│   ├── marketplace_account.py
│   └── ...
│
├── schemas/                      # Pydantic (request/response)
│   ├── user.py
│   ├── marketplace_account.py
│   └── ...
│
├── repositories/                 # Data access layer
│   ├── user_repository.py
│   ├── product_repository.py
│   └── ...
│
├── integrations/                 # APIs externas
│   ├── shopee/
│   │   ├── client.py
│   │   └── schemas.py
│   ├── mercadolivre/
│   │   ├── client.py
│   │   └── schemas.py
│   ├── facebook/
│   └── ...
│
├── agents/                       # IA Agents
│   ├── base_agent.py
│   ├── scout_agent.py
│   ├── analyst_agent.py
│   ├── ranking_agent.py
│   └── publisher_agent.py
│
├── tasks/                        # Background jobs
│   ├── sync_products.py
│   ├── publish_posts.py
│   └── ...
│
├── core/                         # Configurações centrais
│   ├── settings.py              # Variáveis de ambiente
│   ├── exceptions.py            # Exceções customizadas
│   ├── security.py              # JWT, hashing
│   └── logger.py
│
├── database/                     # Setup do banco
│   ├── session.py
│   ├── base.py
│   └── init_db.py
│
├── constants/                    # Constantes
│   └── categories.py
│
├── utils/                        # Funções utilitárias
│
└── main.py                       # Entry point
```

### Frontend (`frontend/src/`)

```
src/
├── pages/                        # Páginas (rotas)
│   ├── Dashboard.tsx
│   ├── Products.tsx
│   ├── Marketplace.tsx
│   ├── Accounts/
│   │   ├── Accounts.tsx
│   │   └── MercadoLivreCallback.tsx
│   └── ...
│
├── components/                   # Componentes reutilizáveis
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── ProductCard.tsx
│   └── ...
│
├── services/                     # API clients
│   ├── api.ts
│   ├── authService.ts
│   ├── marketplaceService.ts
│   └── ...
│
├── hooks/                        # Custom React hooks
│
├── contexts/                     # React contexts
│
├── types/                        # TypeScript types
│   ├── Product.ts
│   ├── Scout.ts
│   └── ...
│
├── utils/                        # Funções utilitárias
│
├── styles/                       # CSS/SCSS globais
│
├── assets/                       # Imagens, ícones
│
├── routes/
│   └── AppRoutes.tsx            # Definição de rotas
│
├── App.tsx
└── main.tsx
```

---

## 🔄 Fluxo de Dados

### Requisição HTTP

```
1. Frontend (React)
   └─> Faz requisição HTTP para API

2. API Layer (FastAPI)
   └─> Valida request
   └─> Autentica usuário (JWT)
   └─> Roteia para handler

3. Service Layer
   └─> Executa lógica de negócio
   └─> Orquestra múltiplos repositórios
   └─> Chama integrações externas se necessário

4. Repository Layer
   └─> Executa queries no banco
   └─> Retorna dados

5. Response
   └─> Service formata resposta
   └─> API serializa (Pydantic)
   └─> Frontend recebe JSON
```

### Exemplo: Autorizar Mercado Livre

```
1. Frontend clica "Autorizar no Mercado Livre"
   └─> Chama GET /mercadolivre/authorize-url

2. API (mercadolivre.py)
   └─> Chama service.get_authorize_url()

3. Service (mercadolivre_auth_service.py)
   └─> Gera state aleatório
   └─> Monta URL de autorização do ML
   └─> Retorna URL

4. Frontend
   └─> Redireciona usuário para URL do ML
   └─> Usuário autoriza
   └─> ML redireciona para /accounts/ml-callback?code=...&state=...

5. Frontend (MercadoLivreCallback.tsx)
   └─> Extrai code e state da URL
   └─> Chama POST /mercadolivre/callback

6. API (mercadolivre.py)
   └─> Chama service.handle_callback(code, state)

7. Service
   └─> Valida state
   └─> Troca code por access_token (chama ML API)
   └─> Criptografa token
   └─> Salva em marketplace_accounts (via repository)

8. Response
   └─> Retorna sucesso
   └─> Frontend redireciona para Accounts
```

---

## 🔐 Segurança

### Autenticação

- **JWT (JSON Web Tokens)** para autenticação de usuários
- **Access Token** com expiração configurável
- **Refresh Token** para renovação

### Criptografia

- **Fernet** (symmetric encryption) para tokens de marketplaces
- **Bcrypt** para hashing de senhas
- **HTTPS** em produção

### Validação

- **Pydantic** para validação de schemas
- **CORS** configurado para frontend
- **Rate limiting** em endpoints críticos

---

## 🤖 Agents (IA)

### Scout Agent
- Busca produtos em marketplaces
- Analisa tendências
- Identifica oportunidades

### Analyst Agent
- Analisa performance de produtos
- Gera insights
- Recomenda ações

### CEO Agent
- Orquestra outros agents
- Toma decisões estratégicas
- Gera relatórios executivos

### Ranking Agent
- Classifica produtos por potencial
- Calcula scores
- Prioriza ações

### Publisher Agent
- Publica conteúdo automaticamente
- Gerencia cronograma
- Monitora performance

---

## 📊 Modelos de Dados Principais

### User
```python
- id: int (PK)
- email: str (unique)
- password_hash: str
- is_admin: bool
- created_at: datetime
```

### MarketplaceAccount
```python
- id: int (PK)
- user_id: int (FK)
- marketplace: str (shopee, mercado_livre, etc)
- account_id: str
- access_token: str (encrypted)
- refresh_token: str (encrypted)
- created_at: datetime
- updated_at: datetime
```

### Product
```python
- id: int (PK)
- user_id: int (FK)
- marketplace: str
- product_id: str
- title: str
- price: float
- commission: float
- status: str
- created_at: datetime
```

---

## 🔌 Integrações

### Shopee
- GraphQL API
- Busca de produtos
- Sincronização de pedidos

### Mercado Livre
- OAuth 2.0
- REST API
- Busca de produtos
- Gerenciamento de contas

### Facebook
- Graph API
- Publicação automática
- Agendamento de posts

### WhatsApp
- WAHA (WhatsApp HTTP API)
- Envio de mensagens
- Notificações

### Abacus AI
- LLM para geração de conteúdo
- Análise de dados
- Recomendações

---

## 🚀 Deployment

### Desenvolvimento
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Produção
```bash
docker-compose -f docker-compose.yml up -d
# Backend: https://api.trendzone.app
# Frontend: https://app.trendzone.app
```

---

## 📝 Convenções de Código

### Backend (Python)
- **Naming**: snake_case para funções/variáveis
- **Classes**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE
- **Type hints**: Sempre usar
- **Docstrings**: Google style

### Frontend (TypeScript)
- **Naming**: camelCase para variáveis/funções
- **Components**: PascalCase
- **Interfaces**: IPascalCase
- **Enums**: PascalCase
- **Constants**: UPPER_SNAKE_CASE

---

## 🧪 Testes

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm run test
```

---

## 📚 Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
