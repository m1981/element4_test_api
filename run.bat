@echo off
REM Fetch the latest git tag
for /f "delims=" %%i in ('git describe --tags --dirty') do @set VERSION=%%i

REM Replace the version in version.py
echo __version__ = "%VERSION%" > version.py

"C:\Users\nakiewic\AppData\Local\Programs\Python\Python311\python.exe"  orders_receiver.py --status processing
pause
