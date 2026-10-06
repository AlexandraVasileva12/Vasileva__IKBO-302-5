@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo === VFS: несколько файлов ===
python emulator.py --vfs vfs_files

pause