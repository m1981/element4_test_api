@echo off
REM Fetch the latest git tag
for /f "delims=" %%i in ('git describe --tags --dirty') do @set VERSION=%%i

REM Replace the version and build date/time in version.py
echo __version__ = "%VERSION%" > version.py
echo __build_date__ = "Now" >> version.py
echo __build_time__ = "Now" >> version.py


"C:\Program Files\Python311\python.exe" orders_receiver.py --status processing
pause
