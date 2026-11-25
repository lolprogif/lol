@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Preparar VLC Portatil - LOI CATFARM PRO
if exist "%~dp0_internal" (set "VLC_DIR=%~dp0_internal\VLC_Portable") else (set "VLC_DIR=%~dp0VLC_Portable")
set "ZIP=%TEMP%\loi_vlc_3.0.24_win64.zip"
set "URL=https://get.videolan.org/vlc/3.0.24/win64/vlc-3.0.24-win64.zip"
set "SHA256=fcf30850371ad10c9373cc4f0f4501e7dee49e3e9ae9f20c72fb2661a1ca6323"

REM Se ja existe uma DLL VLC na pasta portatil, nao baixa novamente.
if exist "%VLC_DIR%\vlc-3.0.24\libvlc.dll" goto :ready
if exist "%VLC_DIR%\libvlc.dll" goto :ready

 echo.
echo Preparando o VLC portatil oficial (aprox. 83 MB)...
echo O download e feito uma unica vez. Nao instala VLC no Windows.
if not exist "%VLC_DIR%" mkdir "%VLC_DIR%"
if exist "%ZIP%" del /q "%ZIP%" >nul 2>nul

where curl.exe >nul 2>nul
if errorlevel 1 goto :no_curl
curl.exe -fL --retry 3 --retry-delay 2 --connect-timeout 20 -o "%ZIP%" "%URL%"
if errorlevel 1 goto :download_error

REM Confere tamanho e SHA-256 para impedir que uma pagina HTML/ZIP incompleto seja aceito.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$f=Get-Item -LiteralPath '%ZIP%' -ErrorAction Stop; if($f.Length -lt 60000000){Write-Error ('Download incompleto: '+$f.Length+' bytes'); exit 2}; $h=(Get-FileHash -LiteralPath '%ZIP%' -Algorithm SHA256).Hash.ToLower(); if($h -ne '%SHA256%'){Write-Error ('SHA-256 invalido: '+$h); exit 3}; exit 0"
if errorlevel 1 goto :invalid_zip

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%VLC_DIR%' -Force -ErrorAction Stop; exit 0 } catch { Write-Error $_; exit 1 }"
if errorlevel 1 goto :extract_error

REM So confirma sucesso se a biblioteca principal realmente foi extraida.
if exist "%VLC_DIR%\vlc-3.0.24\libvlc.dll" goto :cleanup_ready
if exist "%VLC_DIR%\libvlc.dll" goto :cleanup_ready
for /r "%VLC_DIR%" %%F in (libvlc.dll) do if exist "%%F" goto :cleanup_ready
goto :extract_error

:cleanup_ready
del "%ZIP%" >nul 2>nul
goto :ready
:ready
echo.
echo VLC portatil pronto e conferido.
exit /b 0
:no_curl
echo ERRO: curl.exe nao foi encontrado. Atualize o Windows ou baixe o VLC ZIP manualmente.
exit /b 1
:download_error
echo ERRO: falha no download do VLC oficial. Confira a internet e tente novamente.
if exist "%ZIP%" del /q "%ZIP%" >nul 2>nul
exit /b 1
:invalid_zip
echo ERRO: o arquivo baixado esta incompleto ou nao passou na verificacao SHA-256.
if exist "%ZIP%" del /q "%ZIP%" >nul 2>nul
exit /b 1
:extract_error
echo ERRO: o VLC nao foi extraido corretamente. A pasta nao sera considerada pronta.
if exist "%ZIP%" del /q "%ZIP%" >nul 2>nul
exit /b 1
