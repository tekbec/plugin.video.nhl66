@echo off
set addon_root=%~dp0
rmdir /S /Q "%addon_root%codequick"
rmdir /S /Q "%addon_root%_zip"
del "%addon_root%urlquick.py"
exit /b