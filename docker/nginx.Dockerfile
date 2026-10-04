FROM nginx:1.25-alpine

# Remover configuração padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copiar configuração customizada
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Criar diretório para Let's Encrypt
RUN mkdir -p /var/www/certbot

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
