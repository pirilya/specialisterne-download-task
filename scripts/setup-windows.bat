@echo off
cd ..
echo "Setting up..."
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -q -r python\requirements.txt
echo.
echo "Setup complete! Press any key to close this window"
pause >nul