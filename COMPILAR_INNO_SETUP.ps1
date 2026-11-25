$ErrorActionPreference = 'Stop'
$iss = Join-Path $PSScriptRoot 'LOICatFarmPro.iss'
if (!(Test-Path -LiteralPath $iss -PathType Leaf)) { Write-Error "Script ISS nao encontrado: $iss"; exit 3 }
$candidates = @(
  'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
  'C:\Program Files\Inno Setup 6\ISCC.exe',
  (Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe'),
  (Join-Path $env:LOCALAPPDATA 'Inno Setup 6\ISCC.exe')
)
$compiler = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } | Select-Object -First 1
if (!$compiler) {
  foreach ($key in @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')) {
    try {
      $app = Get-ItemProperty $key -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like '*Inno Setup*' -and $_.InstallLocation } | Select-Object -First 1
      if ($app) { $candidate = Join-Path $app.InstallLocation 'ISCC.exe'; if (Test-Path -LiteralPath $candidate -PathType Leaf) { $compiler = $candidate; break } }
    } catch {}
  }
}
if (!$compiler) { Write-Error 'ISCC.exe nao encontrado. Instalacao do Inno Setup pode estar em local diferente.'; exit 2 }
Write-Host "ISCC selecionado: $compiler"
& $compiler $iss
exit $LASTEXITCODE
