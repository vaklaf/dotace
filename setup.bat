@echo off
setlocal

set /p "targetDir=Zadejte cílovou složku pro stažení a rozbalení projektu: "
if not exist "%targetDir%" mkdir "%targetDir%"
cd /d "%targetDir%"

set "githubRepo=VAŠE_UŽIVATELSKÉ_JMÉNO/NÁZEV_REPOSITARE"
set "zipUrl=https://github.com/%githubRepo%/archive/refs/heads/main.zip"
set "projectName=%githubRepo:*/=%"

echo Stahuji archiv z GitHubu...
curl -L "%zipUrl%" -o "%projectName%-main.zip"
if errorlevel 1 goto :error

echo Rozbaluji archiv...
powershell -Command "Expand-Archive -Path '%projectName%-main.zip' -DestinationPath '.'"
if errorlevel 1 goto :error

rem Přejmenování rozbalené složky (pokud je potřeba)
if exist "%projectName%-main" (
    ren "%projectName%-main" "%projectName%"
)

cd "%projectName%"

echo Vytvářím virtuální prostředí...
python -m venv venv
if errorlevel 1 goto :error

echo Aktivuji virtuální prostředí...
call venv\Scripts\activate

echo Instaluji balíčky z requirements.txt...
pip install -r requirements.txt
if errorlevel 1 goto :error

echo Nastavení dokončeno! Nyní můžete spustit 'spustit.bat'.
goto :eof

:error
echo Nastala chyba!
pause
:eof
endlocal