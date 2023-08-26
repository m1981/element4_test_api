@echo off
where python
call "C:\Program Files\Python311\python.exe" -m PyInstaller --onefile orders_receiver.py receipt.py
pause
