@echo off
cd /d "%~dp0"
call "%~dp0PREPARAR_VLC_PORTATIL.bat"
if errorlevel 1 pause & exit /b 1
py loi_catfarm_pro.py
if errorlevel 1 pause
