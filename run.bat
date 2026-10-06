@echo off
chcp 65001 > nul
cd /d "%~dp0"

python src\emulator.py --vfs vfs --script tests\scripts\test_stage5.txt
pause
