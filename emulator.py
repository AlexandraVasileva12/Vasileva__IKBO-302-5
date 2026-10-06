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
    output.config(state="normal") # разрешила писать в экран
    output.insert("end", text + "\n")   # пишу строку в конец экрана
    output.config(state="disabled")     # запретила
    output.see("end")    # прокрутила экран вниз, перешла к новой строке 

write("Параметры запуска:")
write("  VFS: " + str(params.vfs))
write("  Стартовый скрипт: " + str(params.script))

def load_dir(path): # папка читается с диска 
    folder = {}                                    # пустой словарь — это будущая папка
    for name in os.listdir(path):                  # перебираю всё, что лежит в папке на диске
        full_path = os.path.join(path, name)       # полный путь к этому объекту
        if os.path.isdir(full_path):               # если это папка
            folder[name] = load_dir(full_path)     # загружаю её так же, этой же функцией
        else:                                      # иначе это файл
            file = open(full_path, encoding="utf-8", errors="replace")
            folder[name] = file.read()             # кладу в словарь содержимое файла
            file.close()
    return folder                                  # возвращаю готовую папку-словарь

def current_path():
    return "/" + "/".join(cwd)          # список ["home", "alex"] -> строка "/home/alex"

def resolve_path(path):
    if path.startswith("/"):            # путь от корня, например /home/alex
        result = []                     # начинаю с корня
    else:                               # путь от текущей папки, например docs или ..
        result = list(cwd)              # начинаю с копии текущей папки
    for piece in path.split("/"):       # режу путь на кусочки по /
        if piece == "" or piece == ".": # пустой кусок или . (текущая папка) — ничего не делаю
            continue
        elif piece == "..":             # .. — подняться на уровень вверх
            if len(result) > 0:
                result.pop()            # убираю последнюю папку из списка
        else:
            result.append(piece)        # обычное имя — спускаюсь в эту папку
    return result

def get_node(parts):
    node = vfs                          # начинаю с корня VFS
    for name in parts:                  # иду по папкам из списка
        if type(node) != dict or name not in node:
            return None                 # такой папки/файла нет
        node = node[name]               # спускаюсь на уровень ниже
    return node                         # нашла: словарь (папка) или строка (файл)

def ls(args):
    if len(args) > 1:
        write("ls: слишком много аргументов")
        return False
    if len(args) == 0:
        target = "."                    # без аргументов — текущая папка
    else:
        target = args[0]
    node = get_node(resolve_path(target))
    if node is None:
        write("ls: нет такого файла или каталога: " + target)
        return False
    if type(node) == str:               # это файл — просто пишу его имя
        write(target)
        return True
    for name in sorted(node):           # это папка — пишу всё, что внутри, по алфавиту
        if type(node[name]) == dict:
            write(name + "/")           # папки со слешем на конце
        else:
            write(name)
    return True

def cd(args):
    global cwd                          # буду менять переменную cwd, которая снаружи функции
    if len(args) > 1:
        write("cd: слишком много аргументов")
        return False
    if len(args) == 0:                  # cd без аргументов — в корень
        cwd = []
        return True
    parts = resolve_path(args[0])
    node = get_node(parts)
    if node is None:
        write("cd: нет такого каталога: " + args[0])
        return False
    if type(node) == str:
        write("cd: это не каталог: " + args[0])
        return False
    cwd = parts                         # перехожу: запоминаю новую текущую папку
    return True

def echo(args):
    write(" ".join(args))               # склеиваю аргументы через пробел и вывожу
    return True

def head(args):
    count = 10                          # по умолчанию показываю первые 10 строк
    if len(args) > 0 and args[0] == "-n":   # если указали сколько строк: head -n 3 файл
        if len(args) < 2 or not args[1].isdigit():
            write("head: после -n нужно указать число")
            return False
        count = int(args[1])            # превращаю текст "3" в число 3
        args = args[2:]                 # убираю "-n" и число, остаётся имя файла
    if len(args) == 0:
        write("head: не указан файл")
        return False
    if len(args) > 1:
        write("head: слишком много аргументов")
        return False
    node = get_node(resolve_path(args[0]))
    if node is None:
        write("head: нет такого файла: " + args[0])
        return False
    if type(node) == dict:
        write("head: это каталог, а не файл: " + args[0])
        return False
    lines = node.splitlines()           # режу текст файла на строки
    for line in lines[:count]:          # беру только первые count строк
        write(line)
    return True

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
       return ls(args)
    elif name == "cd":
       return cd(args)
    elif name == "echo":
        return echo(args)
    elif name == "head":
        return head(args)
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
    write(current_path() + "$ " + command)      # показала, что ввели
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
        write(current_path() + "$ " + line)
        parts = parse(line)
        ok = run_command(parts)         # запоминаю, получилось или нет
        if ok == False:
            write("[скрипт] ошибка в строке " + str(number) + ", строка пропущена")
        if parts == ["exit"]:
            return

if params.vfs is None:                             # путь к VFS не указали
    vfs = {                                        # создаю VFS по умолчанию прямо в памяти
        "readme.txt": "Это VFS по умолчанию\n",
        "home": {
            "user": {
                "notes.txt": "Мои заметки\n"
            }
        }
    }
    write("VFS не указана, создана VFS по умолчанию")       
elif not os.path.exists(params.vfs):               # ошибка 1: по этому пути ничего нет
    vfs = {}
    write("Ошибка загрузки VFS: путь не найден: " + params.vfs)
elif not os.path.isdir(params.vfs):                # ошибка 2: это не папка
    vfs = {}
    write("Ошибка загрузки VFS: неверный формат, это не папка: " + params.vfs)
else:                                              # всё хорошо, загружаю с диска
    vfs = load_dir(params.vfs)
    write("VFS загружена из: " + params.vfs)

cwd = []

if params.script is not None:             # если путь к скрипту передали
    run_script(params.script)             # выполняю скрипт

window.mainloop() #запустила окно программы 