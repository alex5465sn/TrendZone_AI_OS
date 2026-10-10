# 📊 Monitoramento e Backup — TrendZone AI OS

Guia completo para configurar monitoramento, backup automático e error tracking.

---

## 1️⃣ Backup Automático (SQLite)

### Setup no Servidor

```bash
# 1. Criar diretório de backups
mkdir -p /home/ubuntu/backups
chmod 755 /home/ubuntu/backups

# 2. Testar script de backup manualmente
/home/ubuntu/TrendZone_AI_OS/scripts/backup.sh

# 3. Agendar backup automático (cron)
crontab -e

# Adicionar a linha (backup diário às 2 da manhã):
0 2 * * * /home/ubuntu/TrendZone_AI_OS/scripts/backup.sh >> /home/ubuntu/backups/cron.log 2>&1
```

### Verificar Backups

```bash
# Listar backups
ls -lh /home/ubuntu/backups/

# Testar integridade de um backup
gzip -t /home/ubuntu/backups/trendzone_backup_20261010_020000.db.gz

# Restaurar um backup (se necessário)
gunzip -c /home/ubuntu/backups/trendzone_backup_20261010_020000.db.gz > /home/ubuntu/TrendZone_AI_OS/backend/trendzone.db.restored
```

### Enviar para Google Cloud Storage (Opcional)

```bash
# 1. Instalar gsutil
curl https://sdk.cloud.google.com | bash

# 2. Autenticar
gcloud auth login

# 3. Criar bucket
gsutil mb gs://trendzone-backups-ricardo/

# 4. Descomentar linha no script backup.sh:
# gsutil cp "$BACKUP_FILE_GZ" "gs://trendzone-backups-ricardo/"

# 5. Testar
gsutil ls gs://trendzone-backups-ricardo/
```

---

## 2️⃣ Sentry — Error Tracking

### Setup

1. **Criar conta Sentry** (gratuita)
   - Ir para https://sentry.io/
   - Sign up com email
   - Criar projeto "TrendZone AI OS"
   - Selecionar "FastAPI"

2. **Copiar DSN**
   - Após criar projeto, você verá um DSN como:
   ```
   https://examplePublicKey@o0.ingest.sentry.io/0
   ```

3. **Adicionar ao `.env` em produção**
   ```bash
   SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
   ENVIRONMENT=production
   ```

4. **Rebuild backend**
   ```bash
   docker compose build backend
   docker compose up -d backend
   ```

### Verificar se Está Funcionando

```bash
# Acessar o backend
curl -X GET https://app.trendzone.app/api/health

# Forçar um erro (para teste)
curl -X GET https://app.trendzone.app/api/discovery/winners?invalid_param=true

# Ir para Sentry e verificar se o erro apareceu
# https://sentry.io/organizations/seu-org/issues/
```

### Configurar Alertas no Sentry

1. Ir para **Alerts** → **Create Alert Rule**
2. Configurar:
   - **When:** An issue is first seen
   - **Then:** Send a notification to Slack/Email
3. Salvar

---

## 3️⃣ UptimeRobot — Monitoramento de Disponibilidade

### Setup

1. **Criar conta UptimeRobot** (gratuita)
   - Ir para https://uptimerobot.com/
   - Sign up com email

2. **Adicionar Monitor**
   - Clique em "Add New Monitor"
   - **Monitor Type:** HTTPS
   - **URL:** https://app.trendzone.app/api/health
   - **Friendly Name:** TrendZone API Health
   - **Check Interval:** 5 minutes
   - **Timeout:** 30 seconds

3. **Configurar Alertas**
   - Ir para **Alerts**
   - Clique em "Add Alert Contact"
   - Selecionar **Email** ou **Slack**
   - Adicionar seu email/webhook do Slack
   - Salvar

4. **Verificar Status**
   - Ir para https://status.trendzone.app (opcional, criar página pública)
   - Ou acessar dashboard do UptimeRobot

---

## 4️⃣ GitHub Actions — CI/CD

### Setup

1. **Fazer push do código**
   ```bash
   git add .
   git commit -m "feat: adiciona backup, sentry e ci/cd"
   git push origin main
   ```

2. **Verificar execução**
   - Ir para https://github.com/seu-usuario/TrendZone_AI_OS/actions
   - Clicar na workflow "CI/CD — TrendZone AI OS"
   - Verificar se passou (✅) ou falhou (❌)

3. **Configurar Notificações**
   - Ir para **Settings** → **Notifications**
   - Ativar "Email notifications for failed workflows"

### O que a CI/CD Faz

- ✅ Roda testes do backend (pytest)
- ✅ Roda testes do frontend (npm test)
- ✅ Verifica tipos TypeScript (tsc --noEmit)
- ✅ Faz build do frontend
- ✅ Scans de segurança (Trivy)
- ✅ Envia coverage para Codecov

---

## 5️⃣ Checklist de Monitoramento

- [ ] Backup automático configurado (cron)
- [ ] Sentry DSN adicionado ao `.env` em produção
- [ ] UptimeRobot monitorando `/api/health`
- [ ] Alertas de email/Slack configurados
- [ ] GitHub Actions rodando com sucesso
- [ ] Teste de restauração de backup feito
- [ ] Documentação atualizada

---

## 6️⃣ Troubleshooting

### Backup não está rodando

```bash
# Verificar se cron está ativo
sudo service cron status

# Ver logs do cron
grep CRON /var/log/syslog | tail -20

# Testar script manualmente
bash -x /home/ubuntu/TrendZone_AI_OS/scripts/backup.sh
```

### Sentry não está recebendo erros

```bash
# Verificar se SENTRY_DSN está no .env
grep SENTRY_DSN /home/ubuntu/TrendZone_AI_OS/.env

# Verificar logs do backend
docker compose logs backend | grep -i sentry

# Forçar um erro para teste
curl -X GET https://app.trendzone.app/api/discovery/winners?invalid=true
```

### UptimeRobot mostra "Down"

```bash
# Verificar se endpoint /health está respondendo
curl -I https://app.trendzone.app/api/health

# Verificar logs do nginx
docker compose logs nginx | tail -50

# Verificar logs do backend
docker compose logs backend | tail -50
```

---

## 7️⃣ Próximos Passos

- [ ] Implementar Redis Cache (Fase 2)
- [ ] Implementar testes automatizados (Fase 2)
- [ ] Implementar alertas de performance (Fase 3)
- [ ] Implementar dashboard de métricas (Fase 4)

---

**Última atualização:** 10 de outubro de 2026  
**Responsável:** Arquiteto de Software
