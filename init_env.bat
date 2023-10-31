@echo off
set addon_root=%~dp0
set zip_path_codequick=%addon_root%codequick.zip
set extract_path_codequick=%addon_root%codequick.zip_extracted
set zip_path_pyxbmct=%addon_root%pyxbmct.zip
set extract_path_pyxbmct=%addon_root%pyxbmct.zip_extracted
set zip_path_inputstreamhelper=%addon_root%inputstreamhelper.zip
set extract_path_inputstreamhelper=%addon_root%inputstreamhelper.zip_extracted

rem Download codequick source code
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/willforde/script.module.codequick/archive/refs/heads/master.zip', '%zip_path_codequick%')"
rem Extract it
call :unzip "%extract_path_codequick%" "%zip_path_codequick%"
rem Move required files for the IDE
xcopy "%extract_path_codequick%\script.module.codequick-master\script.module.codequick\lib" "%addon_root%" /e /r /y
rem Delete extracted files
rmdir /S /Q "%extract_path_codequick%"
rem Delete .zip file
del "%zip_path_codequick%"

rem Download pyxbmct source code
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/romanvm/script.module.pyxbmct/archive/refs/heads/master.zip', '%zip_path_pyxbmct%')"
rem Extract it
call :unzip "%extract_path_pyxbmct%" "%zip_path_pyxbmct%"
rem Move required files for the IDE
xcopy "%extract_path_pyxbmct%\script.module.pyxbmct-master\script.module.pyxbmct\lib" "%addon_root%" /e /r /y
rem Delete extracted files
rmdir /S /Q "%extract_path_pyxbmct%"
rem Delete .zip file
del "%zip_path_pyxbmct%"

rem Download inputstreamhelper source code
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/emilsvennesson/script.module.inputstreamhelper/archive/refs/heads/master.zip', '%zip_path_inputstreamhelper%')"
rem Extract it
call :unzip "%extract_path_inputstreamhelper%" "%zip_path_inputstreamhelper%"
rem Move required files for the IDE
if not exist "%addon_root%inputstreamhelper" mkdir "%addon_root%inputstreamhelper"
xcopy "%extract_path_inputstreamhelper%\script.module.inputstreamhelper-master\lib\inputstreamhelper" "%addon_root%inputstreamhelper" /e /r /y
rem Delete extracted files
rmdir /S /Q "%extract_path_inputstreamhelper%"
rem Delete .zip file
del "%zip_path_inputstreamhelper%"
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