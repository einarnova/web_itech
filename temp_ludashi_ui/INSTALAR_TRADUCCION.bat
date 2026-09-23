@echo off
chcp 65001 >nul
echo ================================================
echo   INSTALADOR DE TRADUCCION LUDASHI AL ESPAÑOL
echo ================================================
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Este script necesita ejecutarse como ADMINISTRADOR
    echo.
    echo Haz clic derecho en este archivo y selecciona
    echo "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo [INFO] Permisos de administrador detectados
echo.

:: Cerrar LuDaShi si esta corriendo
echo [PASO 0] Cerrando LuDaShi...
taskkill /F /IM ComputerZTray.exe 2>nul
taskkill /F /IM ComputerZMonHelper.exe 2>nul
taskkill /F /IM ComputerZService.exe 2>nul
taskkill /F /IM ComputerZ_CN.exe 2>nul
taskkill /F /IM computercenter.exe 2>nul
taskkill /F /IM SettingCenter.exe 2>nul
timeout /t 2 >nul

set SRC=C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\final_repacked
set DST=C:\Program Files (x86)\LuDaShi

:: Instalar Themes
echo [PASO 1] Copiando archivos de temas traducidos...
robocopy "%SRC%\Themes" "%DST%\Themes\Default" /E /IS /IT /R:3 /W:1
echo.

:: Instalar DrvMgr defaultskin
echo [PASO 2] Copiando archivos de DrvMgr...
if exist "%SRC%\DrvMgr\defaultskin.ui" (
    copy /Y "%SRC%\DrvMgr\defaultskin.ui" "%DST%\DrvMgr\config\defaultskin\defaultskin.ui"
    echo   Copiado: defaultskin.ui
)
if exist "%SRC%\DrvMgr\LuDaShiFeedback.ui" (
    copy /Y "%SRC%\DrvMgr\LuDaShiFeedback.ui" "%DST%\DrvMgr\feedback\LuDaShiFeedback.ui"
    echo   Copiado: LuDaShiFeedback.ui
)
echo.

echo ================================================
echo   INSTALACION COMPLETADA!
echo   Reinicia LuDaShi para ver los cambios.
echo ================================================
echo.
echo Los archivos originales de respaldo estan en:
echo C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\backup_originals
echo.
pause
