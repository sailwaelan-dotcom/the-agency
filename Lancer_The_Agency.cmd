@echo off
setlocal enabledelayedexpansion
title The Agency - Assistant Solopreneur Belge
chcp 65001 > nul

cd /d "%~dp0"

:: 1. Si l'executable autonome TheAgency.exe est present, le lancer directement (zero Python requis)
if exist "TheAgency.exe" (
    "TheAgency.exe"
    exit /b !ERRORLEVEL!
)

if exist "dist\TheAgency.exe" (
    "dist\TheAgency.exe"
    exit /b !ERRORLEVEL!
)

:: 2. Sinon, detecter l'interpreteur Python disponible (python ou py)
set "PYTHON_CMD="
where python >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=python"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=py"
    )
)

if not defined PYTHON_CMD (
    echo ==========================================================
    echo [ERREUR] Python n'est pas installe sur votre ordinateur.
    echo Rendez-vous sur https://www.python.org/downloads/
    echo ==========================================================
    pause
    exit /b 1
)

%PYTHON_CMD% -m agency
if errorlevel 1 pause
