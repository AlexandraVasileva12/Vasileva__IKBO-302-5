@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo VFS по умолчанию
python src\emulator.py

echo Ошибка: папка VFS не существует
python src\emulator.py --vfs no_vfs

echo Ошибка: вместо папки VFS передан файл
python src\emulator.py --vfs tests\scripts\start.txt
pause
