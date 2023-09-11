@echo on
set BUILD_VERSION=%1
call "C:\\hostedtoolcache\\windows\\Python\\3.11.4\\x64\\python.exe" -m PyInstaller --onefile --name send_sms_%BUILD_VERSION% orders_sms.py
