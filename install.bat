@echo off
:: Create a virtual environment (optional but recommended)
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Install the dependencies
pip install tkinter pillow python-vlc yt-dlp

:: Deactivate the virtual environment
deactivate

echo Dependencies installed successfully!
pause
