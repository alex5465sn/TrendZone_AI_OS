#!/bin/bash

# TrendZone AI OS — Setup SSL/TLS com Let's Encrypt
# Script para configurar certificados HTTPS em produção

set -e

DOMAIN="app.trendzone.app"
EMAIL="ricardonascimento5465@gmail.com"
CERT_DIR="./certs/letsencrypt/live/$DOMAIN"

echo "=========================================="
echo "TrendZone AI OS — Setup SSL/TLS"
echo "=========================================="
echo ""
echo "Domínio: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Criar diretórios
mkdir -p ./certs/letsencrypt
mkdir -p ./certs/certbot

# Verificar se certificado já existe
if [ -f "$CERT_DIR/fullchain.pem" ]; then
    echo "✅ Certificado já existe em $CERT_DIR"
    echo ""
    echo "Para renovar o certificado, execute:"
    echo "  docker compose run --rm certbot renew"
    exit 0
fi

echo "📝 Gerando certificado Let's Encrypt..."
echo ""

# Iniciar Nginx temporariamente para validação
docker compose up -d nginx

# Aguardar Nginx iniciar
sleep 5

# Gerar certificado com Certbot
docker run --rm \
    -v ./certs/letsencrypt:/etc/letsencrypt \
    -v ./certs/certbot:/var/www/certbot \
    -p 80:80 \
    certbot/certbot certonly \
    --standalone \
    --agree-tos \
    --no-eff-email \
    --email "$EMAIL" \
    -d "$DOMAIN"

echo ""
echo "✅ Certificado gerado com sucesso!"
echo ""
echo "Certificado: $CERT_DIR/fullchain.pem"
echo "Chave privada: $CERT_DIR/privkey.pem"
echo ""

# Reiniciar Nginx com SSL
echo "🔄 Reiniciando Nginx com SSL..."
docker compose restart nginx

echo ""
echo "=========================================="
echo "✨ SSL/TLS configurado com sucesso!"
echo "=========================================="
echo ""
echo "Seu site está disponível em: https://$DOMAIN"
echo ""
echo "Para renovar o certificado automaticamente:"
echo "  docker compose run --rm certbot renew --dry-run"
echo ""
