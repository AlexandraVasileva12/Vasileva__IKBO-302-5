@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Запуск со стартовым скриптом
python src\emulator.py --script tests\scripts\start.txt
pause
