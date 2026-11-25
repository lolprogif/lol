@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Criar instalador LOI CATFARM PRO

echo ============================================
echo       LOI CATFARM PRO - GERAR INSTALADOR
echo ============================================
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher nao encontrado. Instale Python 3.11 ou 3.12 64-bit.
  pause
  exit /b 1
)

echo [1/4] Instalando ferramentas de compilacao...
py -m pip install --upgrade pip
py -m pip install pyinstaller keyboard pynput pydirectinput pygetwindow pillow opencv-python-headless numpy python-vlc pywebview
if errorlevel 1 goto :error

echo.
echo [2/4] Limpando compilacao anterior...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist LOICatFarmPro.spec del /q LOICatFarmPro.spec

echo.
echo [3/4] Gerando aplicativo Windows (pasta interna)...
py -m PyInstaller --noconfirm --clean --onedir --windowed ^
 --name LOICatFarmPro ^
 --add-data "spotify_webview_host.py;." ^
 --add-data "inventory_header_template.png;." ^
 --collect-all cv2 --collect-all numpy --collect-all PIL ^
 --collect-all keyboard --collect-all pynput --collect-all pydirectinput ^
 --collect-all pygetwindow --collect-all vlc --collect-all webview ^
 loi_catfarm_pro.py
if errorlevel 1 goto :error

echo.
echo [3b/4] Gerando auxiliar seguro de atualizacao...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name update_helper update_helper.py
if errorlevel 1 goto :error

echo.
echo [4/4] Verificando e preparando Inno Setup 6...
powershell -NoProfile -ExecutionPolicy Bypass -File "INSTALAR_INNO_SETUP6.ps1"
if errorlevel 1 (
  echo Falha ao preparar Inno Setup 6. Confira internet e aceite a autorizacao UAC, se solicitada.
  pause
  exit /b 2
)
REM Compila via script PowerShell dedicado para evitar variaveis de ambiente vazias no CMD.
set "ISCC_SCRIPT=%~dp0COMPILAR_INNO_SETUP.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "%ISCC_SCRIPT%"
if errorlevel 1 goto :error

echo.
echo CONCLUIDO! O instalador esta em:
echo %~dp0Output\LOI_CATFARM_PRO_Setup.exe
pause
exit /b 0

:error
echo.
echo ERRO durante a compilacao. Leia a mensagem acima.
pause
exit /b 1
