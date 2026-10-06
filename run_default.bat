@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Тест 1: запуск без параметров
python emulator.py

pause