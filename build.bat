@echo off
where python
call python -m PyInstaller --onefile orders_receiver.py receipt.py
pause
