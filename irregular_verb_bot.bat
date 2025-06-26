@echo off
chcp 65001
cd /d "%~dp0"

python code/start_bot.py
if errorlevel 1 (
    echo Ошибка при выполнении start_bot.py
    pause
    exit /b 1
)

exit /b