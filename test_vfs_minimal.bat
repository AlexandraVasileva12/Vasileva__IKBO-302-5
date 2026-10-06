@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo VFS с одним файлом
python src\emulator.py --vfs vfs_minimal
pause
