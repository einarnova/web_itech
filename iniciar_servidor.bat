@echo off
title ITECH - Servidor Local
cls
echo ========================================================
echo        ITECH - Servidor de Visualizacion Local
echo ========================================================
echo.
echo Iniciando servidor web local y abriendo navegador...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0servidor.ps1"
pause
