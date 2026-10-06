@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Этап 4: тест команд ls, cd, echo, head
python emulator.py --vfs vfs --script test_stage4.txt

pause