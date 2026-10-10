#!/bin/bash

################################################################################
# TrendZone AI OS — Backup Automático
# 
# Faz backup do banco de dados SQLite e arquivos críticos
# Envia para Google Cloud Storage (ou local)
# Roda via cron: 0 2 * * * /home/ubuntu/TrendZone_AI_OS/scripts/backup.sh
################################################################################

set -e

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

BACKUP_DIR="/home/ubuntu/backups"
DB_PATH="/home/ubuntu/TrendZone_AI_OS/backend/trendzone.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/trendzone_backup_$TIMESTAMP.db"
LOG_FILE="/home/ubuntu/backups/backup.log"

# Retenção: manter últimos 30 dias
RETENTION_DAYS=30

# ============================================================================
# FUNÇÕES
# ============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE"
    exit 1
}

# ============================================================================
# MAIN
# ============================================================================

log "=== Iniciando backup do TrendZone ==="

# Criar diretório se não existir
mkdir -p "$BACKUP_DIR"

# Verificar se banco existe
if [ ! -f "$DB_PATH" ]; then
    error "Banco de dados não encontrado: $DB_PATH"
fi

# Fazer backup do banco
log "Fazendo backup do banco de dados..."
cp "$DB_PATH" "$BACKUP_FILE"
log "Backup salvo em: $BACKUP_FILE"

# Comprimir
log "Comprimindo backup..."
gzip "$BACKUP_FILE"
BACKUP_FILE_GZ="$BACKUP_FILE.gz"
log "Backup comprimido: $BACKUP_FILE_GZ"

# Enviar para Google Cloud Storage (opcional)
# Descomente se tiver gsutil instalado
# log "Enviando para Google Cloud Storage..."
# gsutil cp "$BACKUP_FILE_GZ" "gs://trendzone-backups/"

# Limpar backups antigos (manter últimos 30 dias)
log "Limpando backups antigos (> $RETENTION_DAYS dias)..."
find "$BACKUP_DIR" -name "trendzone_backup_*.db.gz" -mtime +$RETENTION_DAYS -delete
log "Limpeza concluída"

# Verificar integridade do backup
log "Verificando integridade do backup..."
if gzip -t "$BACKUP_FILE_GZ" 2>/dev/null; then
    log "✅ Backup íntegro e pronto"
else
    error "❌ Backup corrompido"
fi

log "=== Backup concluído com sucesso ==="
