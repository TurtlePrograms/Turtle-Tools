@echo off
%~dp0/.venv/Scripts/python.exe -m tt %*
if %errorlevel% neq 0 (
    echo The script failed to execute. Please check for errors.
)