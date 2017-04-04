@setlocal enableextensions
@cd /d "%~dp0"
@echo off

echo Administrative permissions required.
<nul set /p ".=Detecting permissions..."
net session >nul 2>&1
if NOT %errorLevel% == 0 (		
	echo [E R R O R]
	echo Please Run As Admin!
	pause
	goto:eof
) else (
	echo [O K]
)

set PYTHON_DIR=%cd%\python27
set INSTALLATION_DIR=%cd%\installation

<nul set /p ".=Installing python 2.7.13		"
msiexec /i "%INSTALLATION_DIR%\python\python-2.7.13.msi" /quiet /passive TARGETDIR=%PYTHON_DIR% ADDLOCAL=ALL
echo [D O N E]

cls
python "%INSTALLATION_DIR%\installer.py"

rmdir /S /Q %INSTALLATION_DIR%
del install.cmd
