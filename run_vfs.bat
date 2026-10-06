@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Запуск с VFS из папки vfs
python src\emulator.py --vfs vfs
pause
