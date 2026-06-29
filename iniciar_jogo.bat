@echo off
setlocal enabledelayedexpansion
echo ============================================
echo  Missao na Escola - Iniciador
echo ============================================
echo.

set DIR=%~dp0
set PY_DIR=%DIR%python_env
set PY_EXE=%PY_DIR%\python.exe
set PY_ZIP=%DIR%python_env.zip
set GETPIP=%DIR%get-pip.py

REM ── Se o Python portatil ja existe, pula instalacao ──────────
if exist "%PY_EXE%" goto :check_pygame

echo [1/4] Baixando Python portatil (sem precisar instalar)...
echo       Aguarde, pode demorar 1-2 minutos dependendo da internet.
echo.

powershell -NoProfile -Command ^
  "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile '%PY_ZIP%' -UseBasicParsing"

if not exist "%PY_ZIP%" (
    echo ERRO: Falha ao baixar. Verifique a conexao com a internet.
    pause
    exit /b 1
)

echo [2/4] Extraindo Python...
powershell -NoProfile -Command ^
  "Expand-Archive -Path '%PY_ZIP%' -DestinationPath '%PY_DIR%' -Force"
del "%PY_ZIP%"

REM Habilita importacao de modulos externos (edita python311._pth)
for %%f in ("%PY_DIR%\python*._pth") do (
    powershell -NoProfile -Command ^
      "(Get-Content '%%f') -replace '#import site','import site' | Set-Content '%%f'"
)

REM Baixa o get-pip
echo [3/4] Configurando gerenciador de pacotes...
powershell -NoProfile -Command ^
  "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%GETPIP%' -UseBasicParsing"
"%PY_EXE%" "%GETPIP%" --quiet
del "%GETPIP%"

REM Instala pygame
echo [4/4] Instalando pygame...
"%PY_EXE%" -m pip install pygame --quiet --no-warn-script-location

echo.
echo Configuracao concluida! Iniciando o jogo...
echo.
goto :run

:check_pygame
REM Verifica se pygame esta instalado
"%PY_EXE%" -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Instalando pygame...
    "%PY_EXE%" -m pip install pygame --quiet --no-warn-script-location
)

:run
cd /d "%DIR%"
"%PY_EXE%" main.py
if errorlevel 1 (
    echo.
    echo Ocorreu um erro ao iniciar o jogo.
    pause
)
