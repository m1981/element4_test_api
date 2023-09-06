@echo off
call "C:\\hostedtoolcache\\windows\\Python\\3.11.4\\x64\\python.exe" -m PyInstaller --onefile --name %APPNAME% orders_receiver.py receipt.py

REM Local build
REM call "C:\Users\nakiewic\AppData\Local\Programs\Python\Python311\python.exe" -m PyInstaller --onefile --name %APPNAME% orders_receiver.py receipt.py
