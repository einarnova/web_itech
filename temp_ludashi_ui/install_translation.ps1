# Script para instalar los archivos traducidos de LuDaShi
# IMPORTANTE: Ejecutar como Administrador
# Primero cierra LuDaShi completamente antes de ejecutar

$ErrorActionPreference = "Stop"

$repackedDir = "C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\final_repacked"
$ludashiDir = "C:\Program Files (x86)\LuDaShi"
$backupDir = "C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\backup_originals"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  INSTALADOR DE TRADUCCION LUDASHI AL ESPANOL  " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si LuDaShi esta corriendo
$processes = Get-Process -Name "ComputerZ*","ComputerZTray","ComputerZMonHelper","ComputerZService" -ErrorAction SilentlyContinue
if ($processes) {
    Write-Host "[ADVERTENCIA] LuDaShi esta corriendo. Cerrando procesos..." -ForegroundColor Yellow
    $processes | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Paso 1: Crear backup
Write-Host "[PASO 1] Creando backup de archivos originales..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# Backup Themes
$themesSrc = Join-Path $repackedDir "Themes"
if (Test-Path $themesSrc) {
    Get-ChildItem $themesSrc -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($themesSrc.Length + 1)
        $origFile = Join-Path "$ludashiDir\Themes\Default" $rel
        if (Test-Path $origFile) {
            $backupFile = Join-Path $backupDir "Themes\$rel"
            $backupParent = Split-Path $backupFile -Parent
            New-Item -ItemType Directory -Force -Path $backupParent | Out-Null
            Copy-Item $origFile $backupFile -Force
            Write-Host "  Backup: Themes\Default\$rel" -ForegroundColor DarkGray
        }
    }
}

# Backup DrvMgr
$drvmgrSrc = Join-Path $repackedDir "DrvMgr"
if (Test-Path $drvmgrSrc) {
    Get-ChildItem $drvmgrSrc -File | ForEach-Object {
        $origFile = ""
        if ($_.Name -eq "defaultskin.ui") {
            $origFile = "$ludashiDir\DrvMgr\config\defaultskin\defaultskin.ui"
        } elseif ($_.Name -eq "LuDaShiFeedback.ui") {
            $origFile = "$ludashiDir\DrvMgr\feedback\LuDaShiFeedback.ui"
        }
        if ($origFile -and (Test-Path $origFile)) {
            $backupFile = Join-Path $backupDir "DrvMgr\$($_.Name)"
            New-Item -ItemType Directory -Force -Path (Split-Path $backupFile -Parent) | Out-Null
            Copy-Item $origFile $backupFile -Force
            Write-Host "  Backup: DrvMgr\$($_.Name)" -ForegroundColor DarkGray
        }
    }
}

Write-Host "  Backup completado en: $backupDir" -ForegroundColor Green

# Paso 2: Copiar archivos traducidos
Write-Host ""
Write-Host "[PASO 2] Instalando archivos traducidos..." -ForegroundColor Green

# Copiar Themes
if (Test-Path $themesSrc) {
    Get-ChildItem $themesSrc -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($themesSrc.Length + 1)
        $destFile = Join-Path "$ludashiDir\Themes\Default" $rel
        $destParent = Split-Path $destFile -Parent
        New-Item -ItemType Directory -Force -Path $destParent | Out-Null
        Copy-Item $_.FullName $destFile -Force
        Write-Host "  Instalado: Themes\Default\$rel" -ForegroundColor White
    }
}

# Copiar DrvMgr
if (Test-Path $drvmgrSrc) {
    Get-ChildItem $drvmgrSrc -File | ForEach-Object {
        if ($_.Name -eq "defaultskin.ui") {
            $dest = "$ludashiDir\DrvMgr\config\defaultskin\defaultskin.ui"
        } elseif ($_.Name -eq "LuDaShiFeedback.ui") {
            $dest = "$ludashiDir\DrvMgr\feedback\LuDaShiFeedback.ui"
        } else {
            return
        }
        Copy-Item $_.FullName $dest -Force
        Write-Host "  Instalado: DrvMgr\$($_.Name)" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA!" -ForegroundColor Green
Write-Host "  Reinicia LuDaShi para ver los cambios." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Si necesitas restaurar:" -ForegroundColor Yellow
Write-Host "  Los originales estan en: $backupDir" -ForegroundColor Yellow
