@echo off
set addon_root=%~dp0
rmdir /S /Q "%addon_root%codequick"
del "%addon_root%urlquick.py"
exit /b