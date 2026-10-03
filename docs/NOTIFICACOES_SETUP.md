# 🔔 Sistema de Notificações em Tempo Real — Guia de Configuração

## O que foi implementado

Você agora tem um **sistema completo de notificações** que te avisa em tempo real quando cada post é publicado automaticamente. As notificações chegam via:

1. **WhatsApp** — mensagem direta no seu celular
2. **Push Notification** — notificação do navegador/app
3. **Dashboard** — histórico de todas as notificações na plataforma

---

## Como Configurar

### Passo 1: Adicione seu número de WhatsApp ao perfil

1. Acesse **Configurações** (ícone de engrenagem no header)
2. Procure pelo campo **"Número de WhatsApp"**
3. Digite seu número no formato: `+55 11 99999-9999` (com código do país)
4. Salve as alterações

### Passo 2: Teste a conexão

1. Acesse a página **"Plano de Primeira Venda"**
2. Clique em **"Salvar Plano"** (isso dispara uma notificação de teste)
3. Você deve receber uma mensagem no WhatsApp em até 10 segundos

Se não receber:
- Verifique se o número está correto (com código de país +55)
- Certifique-se de que o WhatsApp está ativo no seu celular
- Verifique se o WAHA (serviço de WhatsApp) está rodando no servidor

---

## Como Funciona

### Quando você recebe notificações

**Notificação de Post Publicado:**
```
📱 Post Publicado!

📦 Produto: Palmilha Gel Confortável
📱 Canal: FACEBOOK
⏰ Horário: 14:30:45

Acompanhe em tempo real em: https://app.trendzone.app/first-sale-plan
```

**Notificação de Primeira Venda:**
```
🎉 Primeira Venda!

Parabéns! Você fez sua primeira venda: Palmilha Gel via FACEBOOK
Comissão: R$12.50

Acompanhe em tempo real em: https://app.trendzone.app/first-sale-plan
```

### Onde ver o histórico

1. Clique no **ícone de sino** (🔔) no header
2. Você verá as últimas 10 notificações
3. Clique em qualquer notificação para marcá-la como lida
4. O número vermelho no sino mostra quantas notificações não lidas você tem

---

## Detalhes Técnicos

### Arquitetura

```
Scout (publica post) 
  ↓
NotificationService (envia WhatsApp via WAHA)
  ↓
Notification (registra no banco)
  ↓
Frontend (mostra no sino + histórico)
```

### Endpoints da API

- `GET /notifications` — lista notificações do usuário
- `PUT /notifications/{id}/read` — marca como lida
- `GET /notifications/unread-count` — conta não lidas

### Banco de Dados

Tabela `notifications`:
- `id` — ID único
- `user_id` — seu ID de usuário
- `notification_type` — "whatsapp", "push", "email"
- `title` — título da notificação
- `message` — corpo da mensagem
- `sent` — se foi enviada com sucesso
- `read` — se você já leu
- `created_at` — quando foi criada
- `related_entity_id` — ID do post/venda relacionada

---

## Troubleshooting

### Não estou recebendo notificações no WhatsApp

**Causa 1: Número não configurado**
- Verifique se você adicionou o número em Configurações
- Formato correto: `+55 11 99999-9999`

**Causa 2: WAHA não está rodando**
- SSH no servidor: `docker ps | grep waha`
- Se não aparecer, reinicie: `docker compose up -d waha`

**Causa 3: Número não tem WhatsApp ativo**
- Certifique-se de que o WhatsApp está instalado e ativo no celular
- Tente enviar uma mensagem manualmente para o número via WhatsApp Web

### Estou recebendo muitas notificações

- Você pode desabilitar notificações em Configurações (quando implementado)
- Ou simplesmente ignore o sino — as notificações continuam no histórico

### Notificação chegou atrasada

- WhatsApp pode ter latência de até 30 segundos em conexões lentas
- Isso é normal e esperado

---

## Próximas Melhorias (Roadmap)

- [ ] Notificações por email
- [ ] Configuração de frequência (a cada post, resumo diário, etc.)
- [ ] Notificações de cliques/conversões em tempo real
- [ ] Integração com Telegram
- [ ] Notificações de primeira venda com foto do produto

---

## Suporte

Se tiver problemas:
1. Verifique o número de WhatsApp em Configurações
2. Teste clicando em "Salvar Plano" para disparar uma notificação de teste
3. Verifique os logs do servidor: `docker logs trendzone_backend --since 5m | grep NOTIFICATION`

---

**Commit**: `713d11f` — "feat: adiciona sistema de notificações em tempo real via WhatsApp e Push"

**Data**: 27 de setembro de 2026

**Status**: ✅ Deployado e funcionando em produção
