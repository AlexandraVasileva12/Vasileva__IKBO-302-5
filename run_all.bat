@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Параметры VFS и стартового скрипта
python src\emulator.py --vfs vfs --script tests\scripts\start.txt

echo Параметры в другом порядке
python src\emulator.py --script tests\scripts\start.txt --vfs vfs
pause
