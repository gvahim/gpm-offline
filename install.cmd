@setlocal enableextensions
@cd /d "%~dp0"
@echo off

set PYTHON_DIR=%cd%\python27
set INSTALLATION_DIR=%cd%\installation
set WIRESHARK_DIR=%cd%\wireshark

:InitState
	cls
	Title Gvahim Package Installer - v1.0 & Color 0A
	set /a sstage=0

:check_Permissions
	set /a sstage+=1
	call:Display "Administrative permissions required." "Detecting permissions..." "[i] INFO" %sstage%

    net session >nul 2>&1
    if NOT %errorLevel% == 0 (
		call:Display "Administrative permissions required." "Please Run As Admin" "[e] ERROR !!!" %sstage%
		goto:eof
    )

:pythonInstall
    set /a sstage+=1
    call:Display "Installing Python" "installing..." "[i] INFO" %sstage%
    msiexec /i "%INSTALLATION_DIR%\python\python-2.7.13.msi" /quiet /passive TARGETDIR=%PYTHON_DIR%
    echo installing python - D O N E
    <nul set /p ".=Adding python to path		"
    setx PYTHONPATH "%PYTHON_DIR%;%PYTHON_DIR%\Scripts;" >nul
    echo [D O N E]

    echo installing libraries
    "%PYTHON_DIR%\python.exe" -m pip install --find-links=%INSTALLATION_DIR%\cache --no-index -q colorama

    echo python installer take over
    net session >nul 2>&1

:pythonTakeOver
    "%PYTHON_DIR%\python.exe" installation\installer.py %sstage%
    set /a sstage+=%errorlevel%

:wiresharkPath
    set /a sstage+=1
    call:Display "Setting Wireshark Path" "setting..." "[i] INFO" %sstage%
    setx WIRESHARKPATH "%WIRESHARK_DIR%" >nul

:cleanup
    set /a sstage+=1
    call:Display "Cleanup Environment" "cleaning up...." "[i] INFO" %sstage%
    rmdir /S /Q %INSTALLATION_DIR%
    del install.cmd
    net session >nul 2>&1
    goto:eof

:Display
	cls
	echo /*------------------------------------------------------------------*\
	echo ^|                         - [ Stage %~4 ] -
	echo ^|                   __________________________
	echo ^|
	echo ^|                     Initial Install Script
	echo ^|                   __________________________
	echo ^|
	echo ^|                     * %~1
	echo ^|                     *
	echo ^|                     * %~2
	echo ^|                   __________________________
	echo ^|                   *** %~3 ***
	echo ^|                                                        _\^|/_
	echo ^|                                                        (o o)
	echo \*----------------------------------------------------oOO-{_}-OOo---*/
	rem pause
	PING -n 2 127.0.0.1 > nul
	goto:eof
