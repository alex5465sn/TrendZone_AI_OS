#!/bin/bash
# Deploy TrendZone AI OS na Oracle Cloud VPS
# Executar como: bash deploy-oracle-setup.sh

set -e

echo "=========================================="
echo "TrendZone AI OS - Setup Oracle Cloud VPS"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Update do sistema
echo -e "${YELLOW}[1/8] Atualizando sistema...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar Docker
echo -e "${YELLOW}[2/8] Instalando Docker...${NC}"
sudo apt-get install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# 3. Instalar Git (já deve estar, mas confirma)
echo -e "${YELLOW}[3/8] Verificando Git...${NC}"
git --version

# 4. Clonar repositório
echo -e "${YELLOW}[4/8] Clonando repositório TrendZone...${NC}"
cd /home/ubuntu
if [ ! -d "TrendZone_AI_OS" ]; then
  git clone https://github.com/alex5465sn/TrendZone_AI_OS.git
else
  echo "Repositório já existe, atualizando..."
  cd TrendZone_AI_OS
  git pull origin main
  cd /home/ubuntu
fi

# 5. Configurar .env
echo -e "${YELLOW}[5/8] Configurando variáveis de ambiente...${NC}"
cd /home/ubuntu/TrendZone_AI_OS
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "${RED}ATENCAO: Edite .env com suas credenciais (Shopee, Facebook, etc.)${NC}"
  echo "Arquivo: /home/ubuntu/TrendZone_AI_OS/.env"
  echo ""
  echo "Credenciais necessárias:"
  echo "  - SHOPEE_APP_ID, SHOPEE_SECRET, SHOPEE_ACCESS_TOKEN"
  echo "  - FACEBOOK_PAGE_ID, FACEBOOK_PAGE_TOKEN (opcional)"
  echo "  - SECRET_KEY (JWT - gere uma chave forte)"
  echo ""
  read -p "Pressione ENTER após editar o .env..."
else
  echo ".env já existe, pulando..."
fi

# 6. Configurar firewall (ufw)
echo -e "${YELLOW}[6/8] Configurando firewall (ufw)...${NC}"
sudo ufw --force enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 8000/tcp # Backend (se acessar direto)
sudo ufw status

# 7. Criar diretórios de volume
echo -e "${YELLOW}[7/8] Criando diretórios de volume persistente...${NC}"
mkdir -p /home/ubuntu/TrendZone_AI_OS/backend/media
mkdir -p /home/ubuntu/TrendZone_AI_OS/backend/logs
chmod 755 /home/ubuntu/TrendZone_AI_OS/backend/media
chmod 755 /home/ubuntu/TrendZone_AI_OS/backend/logs

# 8. Subir containers
echo -e "${YELLOW}[8/8] Iniciando containers Docker...${NC}"
cd /home/ubuntu/TrendZone_AI_OS
docker compose up -d --build

echo ""
echo -e "${GREEN}=========================================="
echo "Setup concluído com sucesso!"
echo "==========================================${NC}"
echo ""
echo "Próximos passos:"
echo "1. Verifique se os containers estão rodando:"
echo "   docker ps"
echo ""
echo "2. Veja os logs do backend:"
echo "   docker logs -f trendzone_backend"
echo ""
echo "3. Acesse a API em:"
echo "   http://137.131.248.116:8000/docs"
echo ""
echo "4. Configure um domínio + HTTPS (próximo passo)"
echo ""
