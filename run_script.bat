@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Тест 3: только стартовый скрипт
python emulator.py --script start.txt

pause