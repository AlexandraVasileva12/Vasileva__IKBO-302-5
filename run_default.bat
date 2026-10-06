@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Запуск с VFS по умолчанию
python src\emulator.py
pause
