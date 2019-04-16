@echo off
set curpath=%~dp0

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/

if defined uid (echo UID = %uid%) else set uid=%random%%%32760+1

cd %curpath%
call "kill_server.bat"

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

start %KBE_BIN_PATH%/machine.exe --cid=1888 --gus=1
start %KBE_BIN_PATH%/logger.exe --cid=2888 --gus=2
start %KBE_BIN_PATH%/interfaces.exe --cid=3888 --gus=3
start %KBE_BIN_PATH%/dbmgr.exe --cid=4888 --gus=4
start %KBE_BIN_PATH%/baseappmgr.exe --cid=5888 --gus=5
start %KBE_BIN_PATH%/cellappmgr.exe --cid=6888 --gus=6
start %KBE_BIN_PATH%/baseapp.exe --cid=7888 --gus=7
@rem start %KBE_BIN_PATH%/baseapp.exe --cid=7888 --gus=8 --hide=1
start %KBE_BIN_PATH%/cellapp.exe --cid=8888 --gus=9
@rem start %KBE_BIN_PATH%/cellapp.exe --cid=8888  --gus=10 --hide=1
start %KBE_BIN_PATH%/loginapp.exe --cid=9888 --gus=11