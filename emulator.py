import tkinter as tk #подключаю библиотеку для окна 
import getpass   # чтобы узнать имя пользователя
import socket    # чтобы узнать имя компьютера
import os   # чтобы читать переменные окружения
import argparse   # чтобы читать параметры командной строки

if "HOME" not in os.environ:
    os.environ["HOME"] = os.path.expanduser("~")

parser = argparse.ArgumentParser(description="Эмулятор командной строки")  # создаю «читатель» параметров
parser.add_argument("--vfs", help="путь к папке VFS")                      # параметр 1: путь к VFS
parser.add_argument("--script", help="путь к стартовому скрипту")          # параметр 2: путь к скрипту
params = parser.parse_args()                                                # читаю, что передали при запуске

window = tk.Tk() #создаю главное окно программы
username = getpass.getuser()       # имя пользователя
hostname = socket.gethostname()    # имя компьютера
window.title("Эмулятор - [" + username + "@" + hostname + "]")  # собрали заголовок
window.geometry("700x400") #создала размер окна 

output = tk.Text(window, bg="black", fg="white")
entry = tk.Entry(window, bg="black", fg="white", insertbackground="white")

entry.pack(side="bottom", fill="x")    # сначала строку ввода, прижала к низу
output.pack(fill="both", expand=True)  # потом экран, занимает всё остальное
output.config(state="disabled")        # в экран нельзя печатать руками
entry.focus()                          # курсор сразу в строке ввода


def write(text):
    output.config(state="normal") #разрешила писать в экран
    output.insert("end", text + "\n")   # пишу строку в конец экрана
    output.config(state="disabled")     # запретила
    output.see("end")    #прокрутила экран вниз, перешла к новой строке 

write("Параметры запуска:")
write("  VFS: " + str(params.vfs))
write("  Стартовый скрипт: " + str(params.script))

def expand_vars(text):
    result = "" #собрала готовый текст 
    i = 0 #номер символа, который сейчас смотрим
    while i < len(text):
        if text[i] == "$": 
            i = i + 1
            name = "" #если нашла $, пропустила его и начала собирать имя
            while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                name = name + text[i] #добавляю букву к имени 
                i = i + 1
            if name == "":
                result = result + "$" #если $ без имени, оставляю как есть 
            else:
                result = result + os.environ.get(name, "") #подставляю значение 
        else:
            result = result + text[i]  # обычный символ, просто копируем
            i = i + 1
    return result

def parse(line):
    line = expand_vars(line)   # сначала раскрываю переменные
    return line.split()        # потом режу строку по пробелам на список  

def run_command(parts):
    if len(parts) == 0:     # пользователь просто нажал Enter, ничего не делаем
        return

    name = parts[0]         # первое слово, имя команды
    args = parts[1:]        # всё остальное, аргументы

    if name == "ls":
        write("команда: ls, аргументы: " + " ".join(args)) #вывожу имя и аргументы 
    elif name == "cd":
        if len(args) > 1:   # больше одного аргумента — ошибка
            write("cd: слишком много аргументов")
            return False
        write("команда: cd, аргументы: " + " ".join(args))   # вывожу имя и аргументы
    elif name == "exit":
        if len(args) > 0:   # exit вообще не принимает аргументов
            write("exit: команда не принимает аргументы")
            return False
        window.destroy()    # закрываю окно, программа завершается
    else:                   # ни одно имя не подошло
        write(name + ": команда не найдена") 
        return False
    return True

#если пользователь нажал Enter
def on_enter(event):
    command = entry.get()      # взяла текст из строки ввода
    entry.delete(0, "end")     # сразу очистила строку ввода (переставила сюда)
    write("$ " + command)      # показала, что ввели
    parts = parse(command)     # разбила строку
    run_command(parts)         # выполнила команду

entry.bind("<Return>", on_enter) #<Return> это Enter

def run_script(path):
    # проверка 1: есть ли такой файл
    if not os.path.isfile(path):
        write("Ошибка: файл скрипта не найден: " + path)
        return

    # проверка 2: получается ли его прочитать
    try:
        file = open(path, encoding="utf-8")
        lines = file.readlines()
        file.close()
    except UnicodeDecodeError:
        write("Ошибка: файл скрипта не в кодировке UTF-8: " + path)
        return

    number = 0                          # номер текущей строки в файле
    for line in lines:
        number = number + 1             # каждую строку увеличиваю номер
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        write("$ " + line)
        parts = parse(line)
        ok = run_command(parts)         # запоминаю, получилось или нет
        if ok == False:
            write("[скрипт] ошибка в строке " + str(number) + ", строка пропущена")
        if parts == ["exit"]:
            return

if params.script is not None:             # если путь к скрипту передали
    run_script(params.script)             # выполняю скрипт

window.mainloop() #запустила окно программы 