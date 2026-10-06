@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo VFS с тремя уровнями вложенности
python src\emulator.py --vfs vfs

echo VFS с тремя уровнями и стартовым скриптом
python src\emulator.py --vfs vfs --script tests\scripts\start.txt
pause
