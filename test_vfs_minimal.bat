@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo === VFS: минимальная (один файл) ===
python emulator.py --vfs vfs_minimal

pause