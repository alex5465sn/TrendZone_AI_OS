# Deploy Mercado Livre OAuth Integration to Production
# TrendZone AI OS - Complete Deploy Script

$sshKey = 'C:/Users/alexs/.ssh/ssh-key-2026-09-15 (1).key'
$server = 'ubuntu@137.131.248.116'
$localIntegrations = 'C:/TrendZone_AI_OS/backend/app/integrations'
$remoteBackendPath = '/home/ubuntu/TrendZone_AI_OS/backend/app/'
$remoteProjectPath = '/home/ubuntu/TrendZone_AI_OS'

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  TrendZone AI OS - Mercado Livre OAuth Deploy             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Copy integrations folder
Write-Host "📦 Step 1: Copying integrations folder..." -ForegroundColor Yellow
Write-Host "   From: $localIntegrations" -ForegroundColor Gray
Write-Host "   To:   $server`:$remoteBackendPath" -ForegroundColor Gray
Write-Host ""

scp -r -i $sshKey $localIntegrations $server`:$remoteBackendPath
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Integrations folder copied successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to copy integrations folder" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Rebuild and restart backend
Write-Host "🔨 Step 2: Rebuilding and restarting backend..." -ForegroundColor Yellow
Write-Host "   Server: $server" -ForegroundColor Gray
Write-Host "   Path:   $remoteProjectPath" -ForegroundColor Gray
Write-Host ""

ssh -i $sshKey $server "cd $remoteProjectPath && docker compose build backend && docker compose up -d backend"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend rebuilt and restarted successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to rebuild backend" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Check status and logs
Write-Host "📋 Step 3: Checking status and logs..." -ForegroundColor Yellow
Write-Host ""

ssh -i $sshKey $server "cd $remoteProjectPath && docker compose ps && echo '' && docker compose logs --tail=100 backend"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Deploy Complete!                                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Mercado Livre OAuth integration deployed to production" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Verify backend is running: docker compose ps" -ForegroundColor Gray
Write-Host "2. Test OAuth endpoint: curl https://api.trendzone.app/mercadolivre/authorize-url" -ForegroundColor Gray
Write-Host "3. Check logs if needed: docker compose logs backend" -ForegroundColor Gray
