@echo off
chcp 65001 >nul
echo ========================================
echo  CALCULADORA - BUILD AUTOMÁTICO
echo ========================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

echo [1/5] Verificando ambiente virtual...

:: Cria o venv se não existir
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado com sucesso!
) else (
    echo [OK] Ambiente virtual já existe!
)

echo.
echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado!

echo.
echo [3/5] Instalando dependências...
pip install --upgrade pip >nul 2>&1
pip install pywebview pyinstaller
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências!
    pause
    exit /b 1
)
echo [OK] Dependências instaladas!

echo.
echo [4/5] Limpando builds anteriores...
if exist "build" (
    rmdir /s /q build
    echo [OK] Pasta build removida!
)
if exist "dist" (
    rmdir /s /q dist
    echo [OK] Pasta dist removida!
)
if exist "Calculadora.spec" (
    del /q Calculadora.spec
    echo [OK] Arquivo spec removido!
)

echo.
echo [5/5] Gerando executável...

:: Verifica se o ícone existe
if not exist "icone.ico" (
    echo [AVISO] Arquivo icone.ico não encontrado! Gerando sem ícone...
    pyinstaller --onefile --windowed --name="Calculadora" --clean calculadora.py
) else (
    echo [INFO] Usando icone.ico como ícone do executável...
    pyinstaller --onefile --windowed --icon=icone.ico --name="Calculadora" --clean calculadora.py
)

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar executável!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD CONCLUÍDO COM SUCESSO!
echo ========================================
echo.
echo O executável está em: dist\Calculadora.exe
echo.
echo Tamanho do arquivo:
dir dist\Calculadora.exe | find "Calculadora.exe"
echo.
echo Deseja abrir a pasta dist? (S/N)
set /p resposta="> "
if /i "%resposta%"=="S" (
    explorer dist
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul