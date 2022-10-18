@echo off
cd ..
call .venv\Scripts\activate.bat
python python\download_files.py
echo.
echo "The script is done! Press any key to close this window" &:: prints the ""s too but that's fine hopefully?
pause >nul