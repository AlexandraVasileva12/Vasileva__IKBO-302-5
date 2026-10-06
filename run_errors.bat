@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Ошибка: стартовый скрипт не найден
python src\emulator.py --script nofile.txt

echo Ошибка: вместо скрипта передана папка
python src\emulator.py --script tests

echo Ошибка: неизвестный параметр
python src\emulator.py --unknown value

pause
