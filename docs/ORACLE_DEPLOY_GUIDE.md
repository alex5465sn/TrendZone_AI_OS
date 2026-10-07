# Deploy TrendZone AI OS na Oracle Cloud VPS

## Status Atual ✅
- **IP Público:** `137.131.248.116` (Efêmero, Reservado)
- **Domínio DNS:** `instance-trendzone-server.subnet09150744.vcn09150743.oraclevcn.com`
- **Conexão SSH:** ✅ Testada e funcionando
- **Sistema:** Ubuntu 22.04 LTS, 1 vCPU, 1 GB RAM, 45 GB disco
- **Git:** ✅ Instalado
- **Docker:** ❌ Precisa instalar

---

## Passo 1: Liberar Portas no Security List (Oracle Console)

Antes de rodar o script, libere as portas no firewall da Oracle:

1. Acesse https://cloud.oracle.com → Console
2. Networking → Virtual Cloud Networks → clique na VCN da instância
3. **Listas de Segurança** → clique em "Default Security List"
4. **Adicionar Regras de Entrada** (3 vezes):

| Protocolo | Porta | Origem | Descrição |
|-----------|-------|--------|-----------|
| TCP | 22 | 0.0.0.0/0 | SSH (já deve estar) |
| TCP | 80 | 0.0.0.0/0 | HTTP |
| TCP | 443 | 0.0.0.0/0 | HTTPS |
| TCP | 8000 | 0.0.0.0/0 | Backend (opcional, se acessar direto) |

---

## Passo 2: Executar Script de Setup

Conecte via SSH e rode o script de setup:

```bash
ssh -i ~/.ssh/oracle-trendzone.key ubuntu@137.131.248.116

# Na VPS, execute:
cd /tmp
curl -O https://raw.githubusercontent.com/alex5465sn/TrendZone_AI_OS/main/deploy-oracle-setup.sh
bash deploy-oracle-setup.sh
```

**O que o script faz:**
1. Atualiza o sistema (apt update/upgrade)
2. Instala Docker + Docker Compose
3. Clona o repositório TrendZone
4. Configura firewall (ufw)
5. Cria diretórios de volume persistente
6. Sobe os containers (backend + frontend)

**Tempo estimado:** 5-10 minutos (depende da velocidade da internet)

---

## Passo 3: Configurar Variáveis de Ambiente

Após o script, edite o arquivo `.env` com suas credenciais:

```bash
ssh -i ~/.ssh/oracle-trendzone.key ubuntu@137.131.248.116

# Na VPS:
nano /home/ubuntu/TrendZone_AI_OS/.env
```

**Credenciais obrigatórias:**
- `SHOPEE_APP_ID` — seu App ID da Shopee
- `SHOPEE_SECRET` — seu Secret da Shopee
- `SHOPEE_ACCESS_TOKEN` — token de acesso Shopee
- `SECRET_KEY` — gere uma chave JWT forte (ex: `openssl rand -hex 32`)

**Credenciais opcionais:**
- `FACEBOOK_PAGE_ID` — ID da página Facebook (para posts automáticos)
- `FACEBOOK_PAGE_TOKEN` — token de acesso da página

Após editar, salve (Ctrl+O, Enter, Ctrl+X) e reinicie os containers:

```bash
cd /home/ubuntu/TrendZone_AI_OS
docker compose restart
```

---

## Passo 4: Verificar se Está Rodando

```bash
# Ver containers
docker ps

# Ver logs do backend
docker logs -f trendzone_backend

# Testar API
curl http://137.131.248.116:8000/health
```

Se tudo OK, você verá:
- Backend rodando na porta 8000
- Frontend rodando na porta 4173 (interno)
- Logs sem erros críticos

---

## Passo 5: Configurar HTTPS (Opcional, mas Recomendado)

Se você tiver um **domínio próprio** (ex: `trendzone.com.br`), configure HTTPS com Certbot:

```bash
ssh -i ~/.ssh/oracle-trendzone.key ubuntu@137.131.248.116

# Na VPS:
cd /tmp
curl -O https://raw.githubusercontent.com/alex5465sn/TrendZone_AI_OS/main/deploy-nginx-https.sh
bash deploy-nginx-https.sh seu-dominio.com.br
```

**O que o script faz:**
1. Instala Nginx + Certbot
2. Cria config do Nginx (proxy reverso para o backend)
3. Gera certificado SSL gratuito (Let's Encrypt)
4. Redireciona HTTP → HTTPS automaticamente

Após isso, seu site estará em:
- `https://seu-dominio.com.br` (frontend)
- `https://seu-dominio.com.br/api/` (backend)

---

## Passo 6: Acessar a Plataforma

### Sem domínio (IP direto):
- **API (Swagger):** http://137.131.248.116:8000/docs
- **Frontend:** http://137.131.248.116:4173 (interno, não exposto)

### Com domínio + HTTPS:
- **API (Swagger):** https://seu-dominio.com.br/api/docs
- **Frontend:** https://seu-dominio.com.br

---

## Troubleshooting

### Container não inicia
```bash
docker logs trendzone_backend
docker logs trendzone_frontend
```

### Porta 8000 já em uso
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Sem espaço em disco
```bash
docker system prune -a  # Remove imagens não usadas
```

### Reiniciar tudo
```bash
cd /home/ubuntu/TrendZone_AI_OS
docker compose down
docker compose up -d --build
```

---

## Próximos Passos

1. ✅ Setup Oracle Cloud (você está aqui)
2. ⏳ Integração WhatsApp (WAHA ou Meta Cloud API)
3. ⏳ Configurar domínio + HTTPS
4. ⏳ Backups automáticos do banco de dados

---

## Contato & Suporte

Se algo travar, me mande:
1. Output do `docker logs trendzone_backend`
2. Output do `docker ps`
3. Descrição do erro que viu

Fico à disposição! 🚀
