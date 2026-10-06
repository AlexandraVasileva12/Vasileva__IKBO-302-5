@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo VFS с несколькими файлами
python src\emulator.py --vfs vfs_files
pause
