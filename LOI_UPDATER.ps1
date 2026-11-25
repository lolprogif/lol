param(
  [Parameter(Mandatory=$true)][string]$InstallDir,
  [Parameter(Mandatory=$true)][string]$ZipPath,
  [Parameter(Mandatory=$true)][string]$ExeName
)
$ErrorActionPreference = 'Stop'
$InstallDir = [System.IO.Path]::GetFullPath($InstallDir)
$TempRoot = Join-Path $env:TEMP 'LOI_CATFARM_PRO_updater'
$Stage = Join-Path $TempRoot 'staged'
$Backup = Join-Path $InstallDir ('_backup_update_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
try {
  New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
  if (Test-Path $Stage) { Remove-Item $Stage -Recurse -Force }
  New-Item -ItemType Directory -Force -Path $Stage | Out-Null
  # Wait until the LOI process closes so files are not locked.
  $procName = [System.IO.Path]::GetFileNameWithoutExtension($ExeName)
  while (Get-Process -Name $procName -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 1 }
  Expand-Archive -LiteralPath $ZipPath -DestinationPath $Stage -Force
  if (-not (Test-Path (Join-Path $Stage $ExeName))) { throw "Pacote não contém $ExeName na raiz." }
  New-Item -ItemType Directory -Force -Path $Backup | Out-Null
  Copy-Item -Path (Join-Path $InstallDir '*') -Destination $Backup -Recurse -Force
  Copy-Item -Path (Join-Path $Stage '*') -Destination $InstallDir -Recurse -Force
  Start-Process -FilePath (Join-Path $InstallDir $ExeName) -WorkingDirectory $InstallDir
  Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue
  Remove-Item $TempRoot -Recurse -Force -ErrorAction SilentlyContinue
} catch {
  # Best-effort rollback from the backup if the copy failed.
  if (Test-Path $Backup) {
    Copy-Item -Path (Join-Path $Backup '*') -Destination $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
  }
  Add-Type -AssemblyName PresentationFramework
  [System.Windows.MessageBox]::Show("A atualização falhou. A versão anterior foi restaurada quando possível.\n\n$($_.Exception.Message)", 'LOI CATFARM PRO - Atualizador', 'OK', 'Error') | Out-Null
}
