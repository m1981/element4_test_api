@echo off
where python

REM Fetch the latest git tag
for /f "delims=" %%i in ('git describe --tags --dirty') do @set VERSION=%%i

REM Replace the version in version.py
echo __version__ = "%VERSION%" > version.py

REM Fetch the current date and time
for /f "tokens=2 delims==." %%i in ('wmic os get localdatetime /format:list') do @set datetime=%%i
set BUILD_DATE=%datetime:~6,2%.%datetime:~4,2%.%datetime:~0,4%
set BUILD_TIME=%datetime:~8,2%.%datetime:~10,2%

REM Define application name
set APPNAME=orders_receiver_%VERSION%__built-%BUILD_DATE%__%BUILD_TIME%

REM Replace the version and build date/time in version.py
echo __version__ = "%VERSION%" > version.py
echo __build_date__ = "%BUILD_DATE%" >> version.py
echo __build_time__ = "%BUILD_TIME%" >> version.py

call "C:\Users\nakiewic\AppData\Local\Programs\Python\Python311\python.exe" -m PyInstaller --onefile --name %APPNAME% orders_receiver.py receipt.py version.py
pause
