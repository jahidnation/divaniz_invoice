@echo off

python -c "import jinja2" >nul 2>&1
if %errorlevel% neq 0 (
    pip install jinja2
)

echo Generating...
python divaniz.py

pause
