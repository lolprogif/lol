@echo off
cd /d %~dp0
py -m PyInstaller --onefile --windowed --add-data "spotify_webview_host.py;." --name LOICatFarmPro loi_catfarm_pro.py
echo EXE criado em dist\LOICatFarmPro.exe
pause
