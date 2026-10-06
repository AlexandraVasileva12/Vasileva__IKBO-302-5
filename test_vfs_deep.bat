@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo VFS: 3+ уровня вложенности
python emulator.py --vfs vfs

echo VFS: 3+ уровня вложенности, со стартовым скриптом
python emulator.py --vfs vfs --script start.txt

pause