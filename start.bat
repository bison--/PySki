@echo off

REM Define the virtual environment directory
SET VENV_DIR=venv

REM Check if the virtual environment directory exists
IF NOT EXIST "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
CALL %VENV_DIR%\Scripts\activate

REM Install requirements
IF EXIST "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Run the main Python script
python main.py
