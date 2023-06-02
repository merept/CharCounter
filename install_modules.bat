@echo off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

:start
call :ColorText 0b "install"
call :ColorText 0a " pandas"
echo=
pip install pandas
echo=
call :ColorText 0b "install"
call :ColorText 0a " PyYAML"
echo=
pip install PyYAML
echo=
call :ColorText 0b "install"
call :ColorText 0a " openpyxl"
echo=
pip install openpyxl
echo=
call :ColorText 0a "Install finished"
echo=
pause

goto :eof

:ColorText
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof