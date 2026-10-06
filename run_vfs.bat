@echo off
chcp 65001 > nul
cd /d "%~dp0"

echoТест 2: только путь к VFS
python emulator.py --vfs "%~dp0vfs"

pause