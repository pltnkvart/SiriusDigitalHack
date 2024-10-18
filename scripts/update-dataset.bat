@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PARENT_DIR=%SCRIPT_DIR:~0,-1%"

python "%PARENT_DIR%utils\parser.py" "%PARENT_DIR%datasets\original.xlsx" "%PARENT_DIR%datasets\results.json"

endlocal
