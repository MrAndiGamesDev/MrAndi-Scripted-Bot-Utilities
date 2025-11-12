@echo off
echo Activating virtual environment...
call MrAndi-Scripted-Utilites-Packages\Scripts\activate
echo Virtual environment activated.
timeout /t 1
echo Installing dependencies...
pip install -r requirements.txt
timeout /t 2
echo Dependencies installed.
timeout /t 2
echo Running bot...
python bot.py