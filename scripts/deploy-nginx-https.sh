#!/bin/bash
# Configurar Nginx + HTTPS (Certbot) para TrendZone
# Executar APÓS o setup inicial estar rodando
# Uso: bash deploy-nginx-https.sh seu-dominio.com.br

set -e

DOMAIN="${1:-}"

if [ -z "$DOMAIN" ]; then
  echo "Uso: bash deploy-nginx-https.sh seu-dominio.com.br"
  echo ""
  echo "Exemplo:"
  echo "  bash deploy-nginx-https.sh trendzone.com.br"
  exit 1
fi

echo "=========================================="
echo "Configurando Nginx + HTTPS para: $DOMAIN"
echo "=========================================="
echo ""

# 1. Instalar Nginx e Certbot
echo "[1/5] Instalando Nginx e Certbot..."
sudo apt-get install -y nginx certbot python3-certbot-nginx

# 2. Criar config do Nginx
echo "[2/5] Criando configuração do Nginx..."
sudo tee /etc/nginx/sites-available/trendzone > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Redirecionar HTTP para HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # Certificados SSL (Certbot vai preencher)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    # Configurações SSL recomendadas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Proxy para o backend (Docker)
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Servir frontend (se estiver em /var/www/trendzone)
    location / {
        root /var/www/trendzone;
        try_files \$uri \$uri/ /index.html;
    }

    # Logs
    access_log /var/log/nginx/trendzone_access.log;
    error_log /var/log/nginx/trendzone_error.log;
}
EOF

# 3. Ativar site
echo "[3/5] Ativando site no Nginx..."
sudo ln -sf /etc/nginx/sites-available/trendzone /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

# 4. Gerar certificado SSL
echo "[4/5] Gerando certificado SSL com Certbot..."
sudo certbot certonly --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN

# 5. Iniciar Nginx
echo "[5/5] Iniciando Nginx..."
sudo systemctl enable --now nginx
sudo systemctl restart nginx

echo ""
echo "=========================================="
echo "HTTPS configurado com sucesso!"
echo "=========================================="
echo ""
echo "Seu site está disponível em:"
echo "  https://$DOMAIN"
echo ""
echo "Certificado válido por 90 dias."
echo "Renovação automática: sudo certbot renew --dry-run"
echo ""
