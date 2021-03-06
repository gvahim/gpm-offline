@setlocal enableextensions
@cd /d "%~dp0"
@echo off

set PYTHON_DIR=%cd%\python27
set INSTALLATION_DIR=%cd%\installation
set WIRESHARK_DIR=%cd%\wireshark

if "%1" == "--debug" (
    set PAUSE_CMD=pause
    set DEBUG=true
) else (
    set PAUSE_CMD=net session >nul 2>&1
    set DEBUG=false
)

:InitState
	cls
	Title Gvahim Package Installer - v1.2 & Color 0A
	set /a sstage=0

:check_Permissions
	set /a sstage+=1
	call:Display "Administrative permissions required." "Detecting permissions..." "[i] INFO" %sstage%

    %PAUSE_CMD%
    if NOT %errorLevel% == 0 (
		call:Display "Administrative permissions required." "Please Run As Admin" "[e] ERROR !!!" %sstage%
		goto:eof
    )

:pythonInstall
    set /a sstage+=1
    call:Display "Installing Python" "installing..." "[i] INFO" %sstage%
    msiexec /i "%INSTALLATION_DIR%\softwares\python.msi" /quiet /passive TARGETDIR=%PYTHON_DIR%
    echo Installing Python - D O N E
    <nul set /p ".=Adding python to path		"
    setx PYTHONPATH "%PYTHON_DIR%;%PYTHON_DIR%\Scripts;" /M > nul
    echo [D O N E]

    <nul set /p ".=Check if pip install		"
    "%PYTHON_DIR%\python.exe" -m pip > nul
    if NOT %errorlevel% == 0 (
        echo [B A D]
        <nul set /p ".=Need to install pip. installing...		"
        "%PYTHON_DIR%\python.exe" installation\get-pip.py --find-links=%INSTALLATION_DIR%\cache --no-index > nul
        echo [I N S T A L L E D]
    ) else (
        echo [O K]
    )

    setx PYTHONPATH "%PYTHON_DIR%;%PYTHON_DIR%\Scripts;" /M > nul
    echo [D O N E]

    echo installing libraries
    "%PYTHON_DIR%\python.exe" -m pip install --find-links=%INSTALLATION_DIR%\cache --no-index -q colorama

    %PAUSE_CMD%

:visualCForPython27
    set /a sstage+=1
    call:Display "Installing Visual C++ For Python27" "installing..." "[i] INFO" %sstage%
    msiexec /i "%INSTALLATION_DIR%\softwares\VCForPython27.msi" /quiet /passive
    echo Installing Visual C++ For Python27 - D O N E

    echo python installer take over
    %PAUSE_CMD%

:pythonTakeOver
    Color 07
    if %DEBUG% == true (
        "%PYTHON_DIR%\python.exe" installation\installer.py %sstage% --debug
    ) else (
        "%PYTHON_DIR%\python.exe" installation\installer.py %sstage%
    )
    set /a sstage+=%errorlevel%
    Color 0A

:cleanup
    set /a sstage+=1
    call:Display "Cleanup Environment" "cleaning up...." "[i] INFO" %sstage%
    if %DEBUG% == false (
        rmdir /S /Q %INSTALLATION_DIR%
        del install.cmd
    )
    %PAUSE_CMD%
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
	PING -n 2 127.0.0.1 > nul
	goto:eof
