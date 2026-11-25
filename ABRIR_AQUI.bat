@echo off
title LOI CATFARM PRO - Inicializador
cd /d "%~dp0"

call "%~dp0PREPARAR_VLC_PORTATIL.bat"
if errorlevel 1 (
  echo AVISO: VLC nao preparado neste momento. O LOI vai abrir mesmo assim.
  echo A aba TV tentara preparar o VLC automaticamente quando voce clicar em PLAY.
  echo.
)


REM Solicita permissao de administrador para hooks globais de mouse/teclado.
net session >nul 2>&1
if not "%errorlevel%"=="0" (
  echo Solicitando permissao de administrador para capturar mouse e teclado...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

set PY=
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not defined PY (
  where python >nul 2>nul
  if not errorlevel 1 set PY=python
)
if not defined PY (
  echo Python nao encontrado. Instale Python 3 e tente novamente.
  pause
  exit /b 1
)
%PY% -m pip install keyboard pynput pydirectinput pygetwindow pillow opencv-python-headless numpy python-vlc pywebview
if errorlevel 1 (
  echo Falha ao instalar bibliotecas.
  pause
  exit /b 1
)
%PY% loi_catfarm_pro.py
if errorlevel 1 (
  echo.
  echo O programa fechou com erro. Tire uma foto desta janela e envie.
  pause
)
