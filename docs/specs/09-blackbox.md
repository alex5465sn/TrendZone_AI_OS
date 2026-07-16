# BlackBox Engine

## Objetivo

O BlackBox Engine é responsável por registrar todos os eventos importantes do TrendZone AI OS.

Seu propósito é facilitar:

- Auditoria
- Debug
- Rastreabilidade
- Performance
- Segurança

---

# O que será registrado

## API

- Endpoint chamado
- Método
- Usuário
- Tempo da requisição
- Código HTTP
- Erros

---

## IA

- Prompt enviado
- Modelo utilizado
- Tempo de resposta
- Tokens utilizados
- Resultado

---

## Scout

- Marketplace
- Produto encontrado
- Score calculado
- Tempo da busca

---

## Decision Engine

- Produto
- Score
- Decisão
- Motivo da decisão

---

## Dashboard

- Página aberta
- Tempo de carregamento
- Widgets carregados

---

## Banco de Dados

- Consulta executada
- Tempo
- Erro

---

## Estrutura futura

backend/

app/

core/

blackbox/

logger.py

events.py

metrics.py

tracing.py

---

# Tipos de Logs

INFO

WARNING

ERROR

CRITICAL

AUDIT

AI

---

# Objetivo Final

Qualquer erro ocorrido no sistema deverá ser localizado em menos de 30 segundos.

Nenhuma exceção poderá acontecer sem registro.

Toda decisão importante deverá ser armazenada.