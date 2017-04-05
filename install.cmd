@setlocal enableextensions
@cd /d "%~dp0"
@echo off

::echo Administrative permissions required.
::<nul set /p ".=Detecting permissions..."
::net session >nul 2>&1
::if NOT %errorLevel% == 0 (
::	echo [E R R O R]
::	echo Please Run As Admin!
::	pause
::	goto:eof
::) else (
::	echo [O K]
::)

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

:removeOldInstall
    set /a sstage+=1
    call:Display "Uinstall old gvahim installation" "Uninstalling..." "[i] INFO" %sstage%
    "C:\Heights\PortableApps\InitialSetup\untested_uninstall.bat"
    rmdir /S /Q "C:\Heights\PortableApps\"
    del "C:\Heights\Start.exe"
    if exist "C:\Heights\first.bat" (
        del "C:\Heights\first.*"
    )
    echo Delete Heights folder, keep Documents folder (C:\Heights\Documents)
    net session >nul 2>&1

:pythonInstall
    set /a sstage+=1
    call:Display "Installing Python" "installing..." "[i] INFO" %sstage%
    msiexec /i "%INSTALLATION_DIR%\python\python-2.7.13.msi" /quiet /passive TARGETDIR=%PYTHON_DIR% ADDLOCAL=ALL
    echo installing python - D O N E
    echo adding python to path successfull
    echo python installer take over
    net session >nul 2>&1

:pythonTakeOver
    python installation\installer.py %sstage%
    set /a sstage+=%errorlevel%

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






::set PYTHON_DIR=%cd%\python27
::set INSTALLATION_DIR=%cd%\installation
::
::<nul set /p ".=Installing python 2.7.13		"
::msiexec /i "%INSTALLATION_DIR%\python\python-2.7.13.msi" /quiet /passive TARGETDIR=%PYTHON_DIR% ADDLOCAL=ALL
::echo [D O N E]
::
::cls
::python "%INSTALLATION_DIR%\installer.py"
::
::rmdir /S /Q %INSTALLATION_DIR%
::del install.cmd

pause
