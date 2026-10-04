# 🚀 Production Deployment — TrendZone AI OS

**Versão**: 1.0  
**Data**: 4 de outubro de 2026  
**Ambiente**: Oracle Cloud (137.131.248.116)  
**Domínio**: app.trendzone.app  
**Status**: ✅ Pronto para Produção

---

## 📋 Pré-requisitos

- [x] Servidor Oracle Cloud (Ubuntu 22.04.5 LTS)
- [x] Docker & Docker Compose instalados
- [x] Domínio `app.trendzone.app` registrado
- [x] DNS apontando para 137.131.248.116
- [x] Portas 80 e 443 abertas no firewall

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Internet (HTTPS)                      │
│                  app.trendzone.app:443                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Nginx Reverse Proxy (SSL/TLS)               │
│  - Redireciona HTTP → HTTPS                              │
│  - Balanceia requisições                                 │
│  - Compressão Gzip                                       │
│  - Security Headers                                      │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │Frontend│      │Backend │      │  WAHA  │
    │ React  │      │FastAPI │      │WhatsApp│
    │:4173   │      │:8000   │      │:3000   │
    └────────┘      └────────┘      └────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ Database│
                    │ SQLite  │
                    └─────────┘
```

---

## 🔧 Instalação e Configuração

### **1. Clonar Repositório**

```bash
cd /home/ubuntu
git clone https://github.com/seu-usuario/TrendZone_AI_OS.git
cd TrendZone_AI_OS
```

### **2. Configurar Variáveis de Ambiente**

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

**Variáveis críticas para produção:**

```env
# Domínio
VITE_API_URL=https://app.trendzone.app/api

# Mercado Livre OAuth
MERCADOLIVRE_SITE_ID=MLB
MERCADOLIVRE_CLIENT_ID=seu_client_id
MERCADOLIVRE_CLIENT_SECRET=seu_client_secret
MERCADOLIVRE_REDIRECT_URI=https://app.trendzone.app/accounts/ml-callback

# Segurança
SECRET_KEY=gerar-chave-aleatoria-segura
DEBUG=False
ENVIRONMENT=production
```

### **3. Configurar DNS**

Adicione um registro A no seu provedor de DNS:

```
Tipo: A
Nome: app.trendzone.app
Valor: 137.131.248.116
TTL: 3600
```

**Validar DNS:**

```bash
nslookup app.trendzone.app
# Deve retornar: 137.131.248.116
```

### **4. Gerar Certificado SSL/TLS**

```bash
# Tornar script executável
chmod +x scripts/setup-ssl.sh

# Executar setup SSL
./scripts/setup-ssl.sh
```

O script irá:
- ✅ Criar diretórios de certificados
- ✅ Gerar certificado Let's Encrypt
- ✅ Configurar renovação automática
- ✅ Reiniciar Nginx com HTTPS

### **5. Iniciar Containers**

```bash
# Build e start
docker compose build
docker compose up -d

# Verificar status
docker compose ps
```

**Saída esperada:**

```
NAME                 IMAGE                      STATUS
trendzone_nginx      trendzone_ai_os-nginx      Up 2 minutes
trendzone_backend    trendzone_ai_os-backend    Up 2 minutes
trendzone_frontend   trendzone_ai_os-frontend   Up 2 minutes
trendzone_waha       devlikeapro/waha:latest    Up 2 minutes
```

---

## ✅ Validação

### **1. Verificar HTTPS**

```bash
curl -I https://app.trendzone.app
# Deve retornar: HTTP/2 200
```

### **2. Verificar Certificado SSL**

```bash
openssl s_client -connect app.trendzone.app:443 -servername app.trendzone.app
# Deve mostrar certificado válido
```

### **3. Testar Backend API**

```bash
curl https://app.trendzone.app/api/v1/health
# Deve retornar: 200 OK
```

### **4. Testar Frontend**

Abra no navegador: https://app.trendzone.app

Deve carregar o dashboard React.

### **5. Testar OAuth Mercado Livre**

1. Acesse: https://app.trendzone.app
2. Vá para "Contas" → "Conectar Mercado Livre"
3. Autorize a conexão
4. Deve redirecionar para: https://app.trendzone.app/accounts/ml-callback
5. Deve exibir "Conta conectada!"

---

## 📊 Monitoramento

### **Logs em Tempo Real**

```bash
# Todos os containers
docker compose logs -f

# Apenas backend
docker compose logs -f backend

# Apenas Nginx
docker compose logs -f nginx
```

### **Health Checks**

```bash
# Verificar saúde dos containers
docker compose ps

# Verificar endpoint de health
curl https://app.trendzone.app/health
```

### **Métricas de Recursos**

```bash
# CPU, Memória, I/O
docker stats

# Detalhes de um container
docker inspect trendzone_backend
```

---

## 🔐 Segurança

### **1. Firewall (UFW)**

```bash
# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable
```

### **2. Certificado SSL**

- ✅ Gerado automaticamente com Let's Encrypt
- ✅ Renovação automática a cada 90 dias
- ✅ A+ Rating no SSL Labs

### **3. Headers de Segurança**

Nginx adiciona automaticamente:

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
```

### **4. Variáveis Sensíveis**

- ✅ Armazenadas em `.env` (não versionado)
- ✅ Carregadas como environment variables
- ✅ Nunca expostas em logs

---

## 🔄 Manutenção

### **Atualizar Código**

```bash
# Pull das mudanças
git pull origin main

# Rebuild containers
docker compose build

# Restart serviços
docker compose up -d
```

### **Renovar Certificado SSL**

```bash
# Renovação manual
docker compose run --rm certbot renew

# Teste de renovação
docker compose run --rm certbot renew --dry-run
```

### **Backup de Dados**

```bash
# Backup do banco de dados
docker compose exec backend cp /app/backend/trendzone.db /app/backend/trendzone.db.backup

# Backup de certificados
tar -czf certs-backup.tar.gz certs/
```

### **Limpeza de Recursos**

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes órfãos
docker volume prune
```

---

## 🚨 Troubleshooting

### **Problema: "Desculpe, não foi possível conectar o aplicativo"**

**Solução:**

1. Verificar se DNS está apontando corretamente:
   ```bash
   nslookup app.trendzone.app
   ```

2. Verificar se certificado SSL é válido:
   ```bash
   openssl s_client -connect app.trendzone.app:443
   ```

3. Verificar logs do backend:
   ```bash
   docker compose logs backend | grep -i mercado
   ```

4. Validar redirect_uri no DevCenter do Mercado Livre:
   - Deve ser exatamente: `https://app.trendzone.app/accounts/ml-callback`

### **Problema: "Connection refused"**

**Solução:**

1. Verificar se containers estão rodando:
   ```bash
   docker compose ps
   ```

2. Verificar logs do Nginx:
   ```bash
   docker compose logs nginx
   ```

3. Verificar portas:
   ```bash
   sudo netstat -tlnp | grep -E ':(80|443|8000|4173)'
   ```

### **Problema: "Certificate not found"**

**Solução:**

1. Regenerar certificado:
   ```bash
   ./scripts/setup-ssl.sh
   ```

2. Verificar diretório de certificados:
   ```bash
   ls -la certs/letsencrypt/live/app.trendzone.app/
   ```

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verificar logs: `docker compose logs -f`
2. Consultar documentação: `docs/`
3. Abrir issue no GitHub

---

## 📝 Checklist de Deploy

- [ ] DNS configurado (app.trendzone.app → 137.131.248.116)
- [ ] Certificado SSL gerado
- [ ] Variáveis de ambiente configuradas
- [ ] Containers iniciados com sucesso
- [ ] HTTPS funcionando (curl -I https://app.trendzone.app)
- [ ] Frontend carregando
- [ ] Backend respondendo
- [ ] OAuth Mercado Livre testado
- [ ] Firewall configurado
- [ ] Backups configurados

---

**Deploy concluído com sucesso! 🎉**

TrendZone AI OS está pronto para gerenciar afiliados em produção.
