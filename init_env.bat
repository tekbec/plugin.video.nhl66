@echo off
set addon_root=%~dp0
set zip_path=%addon_root%codequick.zip
set extract_path=%addon_root%codequick.zip_extracted

rem Download codequick source code
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/willforde/script.module.codequick/archive/refs/heads/master.zip', '%zip_path%')"
rem Extract it
call :unzip "%extract_path%" "%zip_path%"
rem Move required files for the IDE
xcopy "%extract_path%\script.module.codequick-master\script.module.codequick\lib" "%addon_root%" /e /r /y
rem Delete extracted files
rmdir /S /Q "%extract_path%"
rem Delete .zip file
del "%zip_path%"
exit /b

:unzip <ExtractTo> <newzipfile>
set vbs="%temp%\_.vbs"
if exist %vbs% del /f /q %vbs%
>%vbs%  echo Set fso = CreateObject("Scripting.FileSystemObject")
>>%vbs% echo If NOT fso.FolderExists(%1) Then
>>%vbs% echo fso.CreateFolder(%1)
>>%vbs% echo End If
>>%vbs% echo set objShell = CreateObject("Shell.Application")
>>%vbs% echo set FilesInZip=objShell.NameSpace(%2).items
>>%vbs% echo objShell.NameSpace(%1).CopyHere(FilesInZip)
>>%vbs% echo Set fso = Nothing
>>%vbs% echo Set objShell = Nothing
cscript //nologo %vbs%
if exist %vbs% del /f /q %vbs%