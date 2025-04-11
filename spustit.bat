@echo off
setlocal

set  "projectDir="."
if not exist "%projectDir%\venv\Scripts\activate" (
    echo Chyba: Virtuální prostředí nebylo nalezeno v zadané složce.
    pause
    goto :eof
)

cd /d "%projectDir%"
call venv\Scripts\activate
echo Spouštím main.py...
python ./main.py

pause
endlocal