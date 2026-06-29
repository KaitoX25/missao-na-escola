@echo off
echo ============================================
echo  Missao na Escola - Gerador de .exe
echo ============================================
echo.

REM Tenta encontrar o Python em varios lugares comuns
set PYTHON=

python --version >nul 2>&1
if not errorlevel 1 ( set PYTHON=python & goto :found )

py --version >nul 2>&1
if not errorlevel 1 ( set PYTHON=py & goto :found )

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON="%LOCALAPPDATA%\Programs\Python\Python312\python.exe" & goto :found )

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON="%LOCALAPPDATA%\Programs\Python\Python311\python.exe" & goto :found )

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON="%LOCALAPPDATA%\Programs\Python\Python310\python.exe" & goto :found )

if exist "C:\Python312\python.exe" ( set PYTHON="C:\Python312\python.exe" & goto :found )
if exist "C:\Python311\python.exe" ( set PYTHON="C:\Python311\python.exe" & goto :found )
if exist "C:\Python310\python.exe" ( set PYTHON="C:\Python310\python.exe" & goto :found )

echo ERRO: Python nao encontrado no computador.
echo.
echo Instale em: https://www.python.org/downloads/
echo IMPORTANTE: na instalacao, marque a opcao "Add Python to PATH"
echo.
pause
exit /b 1

:found
echo Python encontrado: %PYTHON%
%PYTHON% --version
echo.

echo [1/3] Instalando dependencias...
%PYTHON% -m pip install pygame pyinstaller --quiet
if errorlevel 1 (
    echo ERRO ao instalar dependencias. Verifique sua conexao com a internet.
    pause
    exit /b 1
)

echo [2/3] Gerando .exe (pode demorar 2-3 minutos)...
%PYTHON% -m PyInstaller --noconfirm --onedir --windowed --name "Missao_na_Escola" main.py
if errorlevel 1 (
    echo ERRO ao gerar o .exe.
    pause
    exit /b 1
)

echo [3/3] Concluido!
echo.
echo ===========================================
echo  Arquivo gerado em:
echo  dist\Missao_na_Escola\Missao_na_Escola.exe
echo ===========================================
echo.
echo Compacte a pasta dist\Missao_na_Escola\ e entregue ao professor.
echo.
pause
