@Echo off
REM Written by Brendan, Copyright 2014 | All Rights Reserved
REM About: This script turns the layout *.ui files for the GUI of this program into compiled *.py files.

REM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
REM !! SET THESE PATHS TO REFLECT YOUR SYSTEM !!
REM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SET PYTHON=C:\Python27\python.exe
SET PYUIC=C:\Python27\Lib\site-packages\PyQt4\uic\pyuic.py
SET PYRCC=C:\Python27\Lib\site-packages\PyQt4\pyrcc4.exe

REM Clear the screen before we start
cls

REM Set the color of the CMD terminal
color 0A

REM These paths are structured against the project file structure and should not be different system to system (assuming you didn't move things around of course. :p )
SET TWPYDIR=..\..\cmopm\gui\generated
SET TWUIDIR=..\ui
SET MAINUI=%TWUIDIR%\MainWindow_v1.ui
SET MAINPY=%TWPYDIR%\MainWindow_generated.py
SET USERGUIDEUI=%TWUIDIR%\UserGuideWindow_v1.ui
SET USERGUIDEPY=%TWPYDIR%\UserGuideWindow_generated.py
SET ABOUTUI=%TWUIDIR%\AboutWindow_v1.ui
SET ABOUTPY=%TWPYDIR%\AboutWindow_generated.py
SET PREFERENCESUI=%TWUIDIR%\PreferencesWindow_v1.ui
SET PREFERENCESPY=%TWPYDIR%\PreferencesWindow_generated.py
SET RESOURCESQRC=%TWUIDIR%\compiled\resources.qrc
SET RESOURCESPY=%TWPYDIR%\resources_rc.py

REM Show initial header dialog
Echo +---------------------------------------+
Echo ^|        Brendan's CMOPM Compiler       ^|
Echo ^|                                       ^|
Echo ^|                [Notice]               ^|
Echo ^|  Must set PYTHON, PYUIC, PYRCC first  ^|
Echo ^|   Modify them to work on your system  ^|
Echo ^|                                       ^|
Echo ^|   ... Press any key to continue ...   ^|
Echo +---------------------------------------+

REM Wait for user input
pause > nul

REM Compile the Main window ".ui" file to a valid ".py" file
Echo +------------------------------+
Echo ^| Now Compiling Main Window... ^|
Echo +------------------------------+

%PYTHON% %PYUIC% %MAINUI% -o %MAINPY%

REM Compile the User Guide window ".ui" file to a valid ".py" file
Echo +------------------------------------+
Echo ^| Now Compiling User Guide Window... ^|
Echo +------------------------------------+

%PYTHON% %PYUIC% %USERGUIDEUI% -o %USERGUIDEPY%

REM Compile the About window ".ui" file to a valid ".py" file
Echo +-------------------------------+
Echo ^| Now Compiling About Window... ^|
Echo +-------------------------------+

%PYTHON% %PYUIC% %ABOUTUI% -o %ABOUTPY%

REM Compile the Preferences window ".ui" file to a valid ".py" file
Echo +-------------------------------------+
Echo ^| Now Compiling Preferences Window... ^|
Echo +-------------------------------------+

%PYTHON% %PYUIC% %PREFERENCESUI% -o %PREFERENCESPY%

REM Compile the icons resource file ".qrc" to a valid ".py" file so the GUI can use the contained assets
Echo +---------------------------------+
Echo ^| Now Compiling Image Assets...   ^|
Echo +---------------------------------+

%PYRCC% %RESOURCESQRC% -o %RESOURCESPY%

Echo +----------------------+
Echo ^|  Finished Compiling! ^|
Echo +----------------------+

pause

REM Some final clean up (Fix colors, and clear screen)
cls
color

Rem EOF
