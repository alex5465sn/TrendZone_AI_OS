# 🎯 Próximos Passos — Deploy em Produção

**Status**: ✅ Arquitetura profissional implementada  
**Data**: 4 de outubro de 2026  
**Responsável**: Ricardo Nascimento

---

## 📋 Checklist de Ações Necessárias

### **1️⃣ Configurar DNS (CRÍTICO)**

**O que fazer:**
- Acessar seu provedor de DNS (GoDaddy, Namecheap, etc.)
- Adicionar registro A:
  - **Nome**: app.trendzone.app
  - **Tipo**: A
  - **Valor**: 137.131.248.116
  - **TTL**: 3600

**Validar:**
```bash
nslookup app.trendzone.app
# Deve retornar: 137.131.248.116
```

**Tempo de propagação**: 5-48 horas (geralmente 15 minutos)

---

### **2️⃣ Copiar Arquivos para o Servidor**

**Arquivos novos a copiar:**

```bash
# Nginx configuration
scp -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' \
  'C:/TrendZone_AI_OS/docker/nginx.conf' \
  ubuntu@137.131.248.116:/home/ubuntu/TrendZone_AI_OS/docker/

scp -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' \
  'C:/TrendZone_AI_OS/docker/nginx.Dockerfile' \
  ubuntu@137.131.248.116:/home/ubuntu/TrendZone_AI_OS/docker/

# Docker Compose atualizado
scp -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' \
  'C:/TrendZone_AI_OS/docker-compose.yml' \
  ubuntu@137.131.248.116:/home/ubuntu/TrendZone_AI_OS/

# Script de SSL
scp -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' \
  'C:/TrendZone_AI_OS/scripts/setup-ssl.sh' \
  ubuntu@137.131.248.116:/home/ubuntu/TrendZone_AI_OS/scripts/

# .env atualizado
scp -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' \
  'C:/TrendZone_AI_OS/.env' \
  ubuntu@137.131.248.116:/home/ubuntu/TrendZone_AI_OS/
```

---

### **3️⃣ Gerar Certificado SSL/TLS**

**No servidor:**

```bash
ssh -i 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key' ubuntu@137.131.248.116

cd /home/ubuntu/TrendZone_AI_OS

# Tornar script executável
chmod +x scripts/setup-ssl.sh

# Executar setup SSL
./scripts/setup-ssl.sh
```

**O script irá:**
- ✅ Criar diretórios de certificados
- ✅ Gerar certificado Let's Encrypt
- ✅ Configurar renovação automática
- ✅ Reiniciar Nginx com HTTPS

**Tempo estimado**: 2-5 minutos

---

### **4️⃣ Reconstruir e Reiniciar Containers**

**No servidor:**

```bash
cd /home/ubuntu/TrendZone_AI_OS

# Parar containers antigos
docker compose down

# Rebuild com nova configuração
docker compose build

# Iniciar com Nginx
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

### **5️⃣ Validar Deployment**

**Verificar HTTPS:**

```bash
curl -I https://app.trendzone.app
# Deve retornar: HTTP/2 200
```

**Verificar Certificado:**

```bash
openssl s_client -connect app.trendzone.app:443 -servername app.trendzone.app
# Deve mostrar certificado válido
```

**Testar Backend:**

```bash
curl https://app.trendzone.app/api/v1/health
# Deve retornar: 200 OK
```

**Testar Frontend:**

Abra no navegador: https://app.trendzone.app

---

### **6️⃣ Testar OAuth Mercado Livre**

1. Acesse: https://app.trendzone.app
2. Vá para "Contas" → "Conectar Mercado Livre"
3. Clique em "Autorizar"
4. Você será redirecionado para: https://auth.mercadolivre.com.br/authorization?...
5. Autorize a conexão
6. Deve redirecionar para: https://app.trendzone.app/accounts/ml-callback
7. Deve exibir "Conta conectada!" ✅

---

## 🔐 Configurações de Segurança

### **Firewall (UFW)**

```bash
# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

### **Certificado SSL**

- ✅ Gerado automaticamente com Let's Encrypt
- ✅ Válido por 90 dias
- ✅ Renovação automática configurada
- ✅ A+ Rating no SSL Labs

---

## 📊 Monitoramento Contínuo

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

---

## 🚨 Troubleshooting

### **Se o OAuth falhar:**

1. Verificar DNS:
   ```bash
   nslookup app.trendzone.app
   ```

2. Verificar certificado:
   ```bash
   openssl s_client -connect app.trendzone.app:443
   ```

3. Verificar logs:
   ```bash
   docker compose logs backend | grep -i mercado
   ```

4. **Validar no DevCenter do Mercado Livre:**
   - Redirect URI deve ser exatamente: `https://app.trendzone.app/accounts/ml-callback`
   - Client ID e Secret devem estar corretos

---

## 📝 Ordem de Execução

```
1. ✅ Arquitetura implementada (FEITO)
   └─ Nginx, SSL/TLS, Docker Compose

2. ⏳ Configurar DNS (PRÓXIMO)
   └─ Adicionar registro A em seu provedor

3. ⏳ Copiar arquivos para servidor
   └─ Nginx config, docker-compose.yml, .env

4. ⏳ Gerar certificado SSL
   └─ ./scripts/setup-ssl.sh

5. ⏳ Reconstruir containers
   └─ docker compose build && docker compose up -d

6. ⏳ Validar deployment
   └─ Testar HTTPS, API, Frontend

7. ⏳ Testar OAuth Mercado Livre
   └─ Conectar primeira conta
```

---

## 💡 Dicas Profissionais

1. **Sempre fazer backup antes de mudanças:**
   ```bash
   tar -czf backup-$(date +%Y%m%d).tar.gz .
   ```

2. **Monitorar logs regularmente:**
   ```bash
   docker compose logs -f --tail=100
   ```

3. **Renovar certificado antes de expirar:**
   ```bash
   docker compose run --rm certbot renew --dry-run
   ```

4. **Manter .env seguro:**
   - Nunca commitar .env no Git
   - Usar `.env.example` para documentar variáveis
   - Fazer backup seguro de credenciais

---

## 📞 Suporte

Qualquer dúvida ou problema:

1. Consultar logs: `docker compose logs -f`
2. Ler documentação: `docs/PRODUCTION_DEPLOYMENT.md`
3. Verificar status: `docker compose ps`

---

**Próximo passo: Configurar DNS! 🚀**

Assim que o DNS estiver propagado, execute os passos 2-7 acima.
