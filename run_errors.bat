@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo === Тест 6: файл скрипта не существует ===
python emulator.py --script nofile.txt

echo === Тест 7: вместо файла скрипта указана папка ===
python emulator.py --script "%~dp0"

echo === Тест 8: неизвестный параметр ===
python emulator.py --abc 123

echo === Тест 9: справка по параметрам ===
python emulator.py -h

pause