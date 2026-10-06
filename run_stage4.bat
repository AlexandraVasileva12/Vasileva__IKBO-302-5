@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Этап 4: ls, cd, echo, head
python src\emulator.py --vfs vfs --script tests\scripts\test_stage4.txt
pause
