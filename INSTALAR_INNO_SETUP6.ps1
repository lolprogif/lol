$ErrorActionPreference = 'Stop'

function Find-ISCC {
    $pf = [Environment]::GetEnvironmentVariable('ProgramFiles')
    $pf86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    $la = [Environment]::GetEnvironmentVariable('LOCALAPPDATA')
    $roots = @()
    if ($pf) { $roots += $pf }
    if ($pf86) { $roots += $pf86 }
    if ($la) { $roots += (Join-Path $la 'Programs') }

    $direct = @()
    if ($pf) { $direct += (Join-Path $pf 'Inno Setup 6\ISCC.exe') }
    if ($pf86) { $direct += (Join-Path $pf86 'Inno Setup 6\ISCC.exe') }
    if ($la) {
        $direct += (Join-Path $la 'Programs\Inno Setup 6\ISCC.exe')
        $direct += (Join-Path $la 'Inno Setup 6\ISCC.exe')
    }
    foreach ($candidate in $direct) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
    }

    foreach ($regPath in @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
    )) {
        try {
            $apps = Get-ItemProperty -Path $regPath -ErrorAction SilentlyContinue
            foreach ($app in $apps) {
                if ($app.DisplayName -like '*Inno Setup*' -and $app.InstallLocation) {
                    $candidate = Join-Path $app.InstallLocation 'ISCC.exe'
                    if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
                }
            }
        } catch { }
    }

    foreach ($root in $roots) {
        if ($root -and (Test-Path -LiteralPath $root -PathType Container)) {
            try {
                $match = Get-ChildItem -LiteralPath $root -Filter 'ISCC.exe' -File -Recurse -ErrorAction SilentlyContinue |
                    Where-Object { $_.FullName -like '*Inno Setup*' } | Select-Object -First 1
                if ($match) { return $match.FullName }
            } catch { }
        }
    }
    try {
        $whereResult = & where.exe ISCC.exe 2>$null | Select-Object -First 1
        if ($whereResult -and (Test-Path -LiteralPath $whereResult -PathType Leaf)) { return $whereResult.Trim() }
    } catch { }
    return $null
}


$found = Find-ISCC
if ($found) {
    Write-Output "ISCC localizado: $found"
    exit 0
}


Write-Output 'Inno Setup 6 nao localizado. Baixando instalador oficial...'
$url = 'https://github.com/jrsoftware/issrc/releases/download/is-6_7_4/innosetup-6.7.4.exe'
$tempInstaller = Join-Path $env:TEMP 'innosetup-6.7.4-official.exe'
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $tempInstaller -UseBasicParsing
    if (!(Test-Path -LiteralPath $tempInstaller) -or (Get-Item -LiteralPath $tempInstaller).Length -lt 1000000) {
        throw 'Download falhou ou arquivo inesperadamente pequeno.'
    }
    Write-Output 'Solicitando autorizacao do Windows (UAC) para instalar Inno Setup 6...'
    $proc = Start-Process -FilePath $tempInstaller -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-' -Verb RunAs -Wait -PassThru
    if ($proc.ExitCode -ne 0) { throw "Instalador retornou codigo $($proc.ExitCode)." }
    Start-Sleep -Seconds 3
    $found = Find-ISCC
    if (!$found) { throw 'Instalacao finalizada, mas ISCC.exe ainda nao foi encontrado.' }
    Write-Output "Inno Setup pronto: $found"
    exit 0
} catch {
    Write-Error $_
    exit 1
} finally {
    if (Test-Path -LiteralPath $tempInstaller) { Remove-Item -LiteralPath $tempInstaller -Force -ErrorAction SilentlyContinue }
}
