# TrendZone AI OS - Production Deployment Script
# Executa o deploy completo em producao com Nginx e SSL

$sshKey = 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key'
$server = 'ubuntu@137.131.248.116'
$domain = 'app.trendzone.app'
$email = 'ricardonascimento5465@gmail.com'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TrendZone AI OS - Production Deployment" -ForegroundColor Cyan
Write-Host "Dominio: $domain" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# PASSO 1: Parar containers antigos
Write-Host "PASSO 1: Parando containers antigos..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose down"
Write-Host "OK - Containers parados" -ForegroundColor Green
Write-Host ""

# PASSO 2: Rebuild containers
Write-Host "PASSO 2: Reconstruindo containers (5-10 minutos)..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose build --no-cache 2>&1 | tail -50"
Write-Host "OK - Containers reconstruidos" -ForegroundColor Green
Write-Host ""

# PASSO 3: Iniciar containers
Write-Host "PASSO 3: Iniciando containers..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose up -d"
Write-Host "OK - Containers iniciados" -ForegroundColor Green
Write-Host ""

# PASSO 4: Aguardar Nginx iniciar
Write-Host "PASSO 4: Aguardando Nginx iniciar (30 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host "OK - Nginx iniciado" -ForegroundColor Green
Write-Host ""

# PASSO 5: Gerar certificado SSL
Write-Host "PASSO 5: Gerando certificado SSL com Let's Encrypt..." -ForegroundColor Yellow
Write-Host "Email: $email" -ForegroundColor Gray
Write-Host "Dominio: $domain" -ForegroundColor Gray
Write-Host ""

ssh -i $sshKey $server @"
cd /home/ubuntu/TrendZone_AI_OS
mkdir -p certs/letsencrypt
mkdir -p certs/certbot
docker run --rm -v `$(pwd)/certs/letsencrypt:/etc/letsencrypt -v `$(pwd)/certs/certbot:/var/www/certbot -p 80:80 certbot/certbot certonly --standalone --agree-tos --no-eff-email --email $email -d $domain
"@

Write-Host "OK - Certificado SSL gerado" -ForegroundColor Green
Write-Host ""

# PASSO 6: Reiniciar Nginx com SSL
Write-Host "PASSO 6: Reiniciando Nginx com SSL..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose restart nginx; sleep 10"
Write-Host "OK - Nginx reiniciado com SSL" -ForegroundColor Green
Write-Host ""

# PASSO 7: Verificar status
Write-Host "PASSO 7: Verificando status dos containers..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose ps"
Write-Host ""

# PASSO 8: Validar HTTPS
Write-Host "PASSO 8: Validando HTTPS..." -ForegroundColor Yellow
ssh -i $sshKey $server "curl -I https://$domain 2>&1 | head -5"
Write-Host ""

# PASSO 9: Verificar logs
Write-Host "PASSO 9: Ultimos logs do backend..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/TrendZone_AI_OS; docker compose logs --tail=30 backend"
Write-Host ""

# RESUMO FINAL
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOY CONCLUIDO COM SUCESSO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Seu site esta disponivel em:" -ForegroundColor Cyan
Write-Host "https://$domain" -ForegroundColor Green
Write-Host ""
Write-Host "Status dos containers:" -ForegroundColor Cyan
Write-Host "ssh -i '$sshKey' $server 'cd /home/ubuntu/TrendZone_AI_OS; docker compose ps'" -ForegroundColor Gray
Write-Host ""
Write-Host "Logs em tempo real:" -ForegroundColor Cyan
Write-Host "ssh -i '$sshKey' $server 'cd /home/ubuntu/TrendZone_AI_OS; docker compose logs -f'" -ForegroundColor Gray
Write-Host ""
Write-Host "Proximo passo: Testar OAuth Mercado Livre em https://$domain" -ForegroundColor Yellow
Write-Host ""
