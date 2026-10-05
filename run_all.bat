@echo off 
chcp 65001 > nul
cd /d "%~dp0" 

echo === Тест 4: оба параметра ===
python emulator.py --vfs "%~dp0vfs" --script start.txt

echo === Тест 5: оба параметра в другом порядке ===
python emulator.py --script start.txt --vfs "%~dp0vfs"

pause