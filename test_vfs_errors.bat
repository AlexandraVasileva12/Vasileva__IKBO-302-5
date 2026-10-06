@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo === VFS не указана: VFS по умолчанию ===
python emulator.py

echo === VFS: папка не существует ===
python emulator.py --vfs novfs

echo === VFS: вместо папки файл ===
python emulator.py --vfs start.txt

pause