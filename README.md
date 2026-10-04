# TrendZone AI OS

**Sistema Operacional de IA para Gerenciamento de Afiliados em Marketplaces**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-darkgreen.svg)](https://fastapi.tiangolo.com/)
[![React 18+](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

---

## 🎯 Sobre

TrendZone AI OS é uma plataforma inteligente que automatiza a gestão de produtos em múltiplos marketplaces. Utiliza IA para análise de tendências, otimização de preços, automação de publicações e geração de conteúdo.

### Principais Funcionalidades

- 🤖 **IA Agents** - Scout, Analyst, CEO, Ranking, Publisher
- 🛍️ **Integrações** - Shopee, Mercado Livre, Facebook, WhatsApp
- 📊 **Dashboard** - Análise em tempo real de produtos e vendas
- 🔐 **OAuth 2.0** - Autenticação segura com marketplaces
- 📱 **Responsivo** - Interface moderna e intuitiva
- 🚀 **Escalável** - Arquitetura em camadas, pronta para produção

---

## 🚀 Quick Start

### Com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/alex5465sn/TrendZone_AI_OS.git
cd TrendZone_AI_OS

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# Inicie a aplicação
docker-compose up -d

# Acesse
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Setup Manual

Veja [docs/SETUP.md](./docs/SETUP.md) para instruções detalhadas.

---

## 📚 Documentação

- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Arquitetura e design do sistema
- **[SETUP.md](./docs/SETUP.md)** - Guia de setup local
- **[DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Guia de deployment em produção
- **[API Docs](http://localhost:8000/docs)** - Documentação interativa (Swagger)

---

## 🏗️ Estrutura do Projeto

```
TrendZone_AI_OS/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # Endpoints REST
│   │   ├── services/          # Lógica de negócio
│   │   ├── models/            # ORM (SQLAlchemy)
│   │   ├── integrations/      # APIs externas
│   │   ├── agents/            # IA Agents
│   │   └── ...
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── pages/             # Páginas
│   │   ├── components/        # Componentes
│   │   ├── services/          # API clients
│   │   ├── routes/            # Rotas
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
│
├── docs/                       # Documentação
├── scripts/                    # Scripts utilitários
├── docker-compose.yml          # Orquestração Docker
└── .env.example                # Template de .env
```

---

## 🔧 Tecnologias

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **Python 3.11+**

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Material-UI** - Component library

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **SQLite** (dev) / **PostgreSQL** (prod) - Banco de dados
- **Redis** (opcional) - Cache
- **RabbitMQ** (opcional) - Message queue

---

## 🔌 Integrações

### Marketplaces
- **Shopee** - GraphQL API, busca de produtos, sincronização
- **Mercado Livre** - OAuth 2.0, REST API, gerenciamento de contas

### Redes Sociais
- **Facebook** - Graph API, publicação automática
- **WhatsApp** - WAHA, envio de mensagens

### IA & LLM
- **Abacus AI** - Geração de conteúdo, análise de dados
- **OpenRouter** - Acesso a múltiplos modelos LLM

---

## 🤖 IA Agents

### Scout Agent
Busca produtos em marketplaces e identifica oportunidades de venda.

### Analyst Agent
Analisa performance de produtos e gera insights.

### CEO Agent
Orquestra outros agents e toma decisões estratégicas.

### Ranking Agent
Classifica produtos por potencial de venda.

### Publisher Agent
Publica conteúdo automaticamente em redes sociais.

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

## 📦 Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
# APP
APP_NAME=TrendZone AI OS
DEBUG=True
ENVIRONMENT=development

# DATABASE
DATABASE_URL=sqlite:///trendzone.db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# SHOPEE
SHOPEE_APP_ID=your-app-id
SHOPEE_SECRET=your-secret

# MERCADO LIVRE
MERCADOLIVRE_CLIENT_ID=your-client-id
MERCADOLIVRE_CLIENT_SECRET=your-secret

# FACEBOOK
FACEBOOK_APP_ID=your-app-id
FACEBOOK_APP_SECRET=your-secret

# ABACUS AI
ABACUS_API_KEY=your-api-key

# OPENROUTER
OPENROUTER_API_KEY=your-api-key
```

---

## 🚀 Deployment

### Produção (Oracle Cloud)

```bash
# SSH para servidor
ssh ubuntu@your-server-ip

# Clone e setup
git clone https://github.com/alex5465sn/TrendZone_AI_OS.git
cd TrendZone_AI_OS
cp .env.example .env
# Configure .env

# Inicie com Docker
docker-compose up -d

# Verifique status
docker-compose ps
docker-compose logs -f backend
```

Veja [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) para detalhes completos.

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -m "feat: descrição"`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](./LICENSE) para detalhes.

---

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma [issue no GitHub](https://github.com/alex5465sn/TrendZone_AI_OS/issues)
- Entre em contato com o time de desenvolvimento

---

## 🙏 Agradecimentos

Desenvolvido com ❤️ por [Alex Serafim](https://github.com/alex5465sn)

---

**Última atualização**: Outubro 2026
