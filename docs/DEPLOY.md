# Deploy da TrendZone AI OS (produção 24h, sem depender do seu PC)

## Visão geral
- **Backend + banco de dados** → VPS gratuita (Oracle Cloud Free Tier), rodando via Docker, sempre ligado.
- **Frontend** → Vercel ou Netlify (grátis).
- O projeto já tem `docker-compose.yml` e Dockerfiles prontos em `docker/`.

## Passo 1 — Criar a VPS gratuita (Oracle Cloud)
1. Crie a conta em https://www.oracle.com/cloud/free/ (cartão pedido só para verificação, não é cobrado no plano Always Free).
2. Crie uma instância "Compute" com a imagem **Ubuntu 22.04**, shape **VM.Standard.E2.1.Micro** (Always Free).
3. Anote o IP público da instância.
4. Libere as portas no Security List/Network Security Group da Oracle: **80**, **443**, **8000**.

## Passo 2 — Preparar o servidor
Conectar via SSH e instalar Docker:
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

## Passo 3 — Subir o código
```bash
git clone https://github.com/alex5465sn/TrendZone_AI_OS.git
cd TrendZone_AI_OS
cp .env.example .env
nano .env   # preencher com os valores reais (Shopee, Facebook, etc.)
```

## Passo 4 — Subir os containers
```bash
docker compose up -d --build
```
Isso deixa o backend rodando permanentemente na porta 8000, reiniciando sozinho se o servidor reiniciar (`restart: unless-stopped`).

## Passo 5 — Frontend (Vercel/Netlify)
1. Importe o repositório no Vercel, apontando a raiz do projeto para `frontend/`.
2. Configure a variável de ambiente do frontend apontando para `http://SEU_IP_DA_VPS:8000` (ou domínio, se tiver).
3. Deploy automático a cada push no `main`.

## Observações
- O agendador de posts e o publicador automático continuam rodando dentro do container do backend, 24h, mesmo com seu PC desligado.
- Os vídeos gerados ficam salvos em `backend/media/` (volume persistente do Docker) e não são versionados no Git.
- Recomenda-se um domínio próprio + HTTPS (Nginx + Certbot ou Cloudflare) antes de divulgar a plataforma publicamente — pode ser um próximo passo.
