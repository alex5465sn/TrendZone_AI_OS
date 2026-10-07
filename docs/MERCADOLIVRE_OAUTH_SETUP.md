# Configuração Completa do OAuth 2.0 do Mercado Livre

## Status Atual ✅

- ✅ Backend: Mercado Livre OAuth integrado e deployado em produção
- ✅ Frontend: Tela de autorização implementada
- ✅ Domínio: `app.trendzone.app` com SSL/TLS válido (Let's Encrypt)
- ✅ Redirect URI: Configurado no DevCenter do Mercado Livre
- ⏳ **Próximo passo**: Completar o fluxo de autorização

---

## Passo a Passo para Autorizar a Conta

### 1. Acessar a Plataforma

```
https://app.trendzone.app
```

Faça login com suas credenciais de administrador.

### 2. Ir para "Contas de Afiliado"

- Clique em **"Afiliado"** no menu lateral
- Selecione **"Contas de Afiliado"**

### 3. Autorizar o Mercado Livre

Você verá um card do Mercado Livre com status **"Pendente"** (após a correção).

Clique no botão **"Conectar"** ou **"Autorizar"**.

### 4. Fazer Login no Mercado Livre

Você será redirecionado para:
```
https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=6584154213136746&...
```

**Importante**: Faça login com a **conta principal/administrador** do Mercado Livre, não com colaborador.

### 5. Autorizar a Aplicação

O Mercado Livre pedirá permissão para que o TrendZone acesse:
- Dados da sua conta
- Produtos publicados
- Pedidos e vendas
- Etc.

Clique em **"Autorizar"** ou **"Permitir"**.

### 6. Redirecionamento Automático

Você será redirecionado de volta para:
```
https://app.trendzone.app/accounts/ml-callback?code=...&state=...
```

O backend trocará o `code` por um `access_token` e `refresh_token` automaticamente.

### 7. Confirmação

Você verá a mensagem:
```
✅ Conta do Mercado Livre conectada com sucesso!
```

E o status mudará para **"Conectada"**.

---

## Troubleshooting

### Erro: "Desculpe, não foi possível conectar o aplicativo à sua conta"

**Causa**: O `redirect_uri` no DevCenter não corresponde exatamente ao configurado no backend.

**Solução**:
1. Acesse https://developers.mercadolivre.com.br/devcenter
2. Abra sua aplicação (client_id: `6584154213136746`)
3. Verifique o campo **"URL de redirect"**
4. Deve ser **exatamente**:
   ```
   https://app.trendzone.app/accounts/ml-callback
   ```
5. Sem barra a mais, sem `www`, sem `http://` (deve ser `https://`)

### Erro: "Token inválido ou expirado"

**Causa**: O token foi revogado ou expirou.

**Solução**: Desconecte e reconecte a conta.

### Nada carrega na aba "Mercado Livre"

**Causa**: Conta ainda está em status "Pendente" (sem token real).

**Solução**: Complete o fluxo de autorização acima.

---

## Endpoints da API

Após autorizar, você pode usar:

### Status da Conexão
```bash
GET /api/mercadolivre/status
Authorization: Bearer <seu_token_jwt>
```

Resposta:
```json
{
  "data": {
    "is_connected": true,
    "user_id": "123456789",
    "email": "seu@email.com",
    "nickname": "seu_nickname"
  }
}
```

### Buscar Produtos
```bash
GET /api/marketplace/search?marketplace=mercado_livre&q=celular&limit=10
Authorization: Bearer <seu_token_jwt>
```

### Refresh Token
```bash
POST /api/mercadolivre/refresh
Authorization: Bearer <seu_token_jwt>
```

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  https://app.trendzone.app/accounts                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 1. Clica "Autorizar"
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  GET /api/mercadolivre/authorize-url                        │
│  → Gera URL com PKCE challenge                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 2. Redireciona para
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Mercado Livre Auth Server                      │
│  https://auth.mercadolivre.com.br/authorization             │
│  → Usuário faz login e autoriza                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 3. Redireciona com ?code=...&state=...
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Callback)                      │
│  https://app.trendzone.app/accounts/ml-callback             │
│  → Extrai code e state da URL                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 4. Envia code para backend
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Callback)                       │
│  GET /api/mercadolivre/callback?code=...&state=...          │
│  → Troca code por access_token + refresh_token              │
│  → Salva tokens no banco (criptografados)                   │
│  → Retorna sucesso                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ 5. Mostra "Conectada!"
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Dashboard)                     │
│  Agora pode buscar produtos, vendas, etc.                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Segurança

- ✅ **PKCE**: Implementado para proteger contra ataques de autorização
- ✅ **State**: Validado para prevenir CSRF
- ✅ **Tokens criptografados**: Salvos com Fernet no banco de dados
- ✅ **HTTPS obrigatório**: Certificado Let's Encrypt válido
- ✅ **Refresh automático**: Tokens expirados são renovados automaticamente

---

## Próximos Passos

1. ✅ Completar autorização do Mercado Livre (você faz isso)
2. ⏳ Implementar busca de produtos do Mercado Livre na aba "Produtos"
3. ⏳ Sincronizar vendas do Mercado Livre
4. ⏳ Gerar links de afiliado do Mercado Livre

---

**Última atualização**: 04/10/2026
**Status**: Pronto para produção ✅
