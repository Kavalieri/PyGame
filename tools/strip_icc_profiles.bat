@echo off
REM Script para eliminar perfiles ICC de todos los PNG en assets y subcarpetas (verbose)
REM Autor: Gemini
REM Fecha: 2024-06-08
REM Descripción: Elimina perfiles ICC corruptos de los PNG y muestra progreso

cd /d %~dp0\..\assets

echo Procesando archivos PNG en: %CD%
echo.

setlocal enabledelayedexpansion
set count=0

for /R %%F in (*.png) do (
    set /a count+=1
    echo Procesando: %%F
    magick identify "%%F" >nul 2>&1
    if errorlevel 1 (
        echo   [ERROR] Archivo no válido o corrupto: %%F
    ) else (
        magick mogrify -strip "%%F"
        if errorlevel 1 (
            echo   [ERROR] No se pudo limpiar: %%F
        ) else (
            echo   [OK] Limpio: %%F
        )
    )
)
echo.
echo Total de archivos procesados: !count!
echo Proceso completado. Si ves errores, revisa los archivos indicados.
pause 