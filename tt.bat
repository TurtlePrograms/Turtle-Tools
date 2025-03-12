@echo off
if not exist "%~dp0/.venv" (
    echo Creating virtual environment...
    python -m venv %~dp0/.venv
    call %~dp0/.venv/Scripts/activate.bat
    python.exe -m pip install --upgrade pip
    pip install -r %~dp0/requirements.txt
    echo Virtual environment created.
)
call %~dp0/.venv/Scripts/activate.bat
python %~dp0/tt.py %*
if %errorlevel% neq 0 (
    echo TT: The script failed to execute.
)