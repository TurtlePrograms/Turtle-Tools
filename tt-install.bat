@REM ask for install path
@echo off
set /p install_path="Enter the path to install the program: "
@REM create the install directory
mkdir %install_path%
@REM copy the files
copy /Y .\tt\* %install_path%
@REM create the virtual environment
cd %install_path%
python -m venv .venv
@REM install the dependencies
call .venv\Scripts\activate
tt install
@REM done
echo The program has been installed to %install_path%.
pause
REM End of file