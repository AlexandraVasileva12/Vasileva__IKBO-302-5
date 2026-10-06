import argparse
import getpass
import os
import socket
import tkinter as tk

MIN_HEAD_ARGUMENTS = 2

if "HOME" not in os.environ:
    os.environ["HOME"] = os.path.expanduser("~")

parser = argparse.ArgumentParser(description="Эмулятор командной строки")
parser.add_argument("--vfs", help="путь к папке VFS")
parser.add_argument("--script", help="путь к стартовому скрипту")
params = parser.parse_args()

window = tk.Tk()
username = getpass.getuser()
hostname = socket.gethostname()
window.title("Эмулятор - [" + username + "@" + hostname + "]")
window.geometry("700x400")

output = tk.Text(window, bg="black", fg="white")
entry = tk.Entry(window, bg="black", fg="white", insertbackground="white")

entry.pack(side="bottom", fill="x")
output.pack(fill="both", expand=True)
output.config(state="disabled")
entry.focus()


def write(text):
    output.config(state="normal")
    output.insert("end", text + "\n")
    output.config(state="disabled")
    output.see("end")


write("Параметры запуска:")
write("  VFS: " + str(params.vfs))
write("  Стартовый скрипт: " + str(params.script))


def load_dir(path):
    folder = {}
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            folder[name] = load_dir(full_path)
        else:
            with open(full_path, encoding="utf-8", errors="replace") as file:
                folder[name] = file.read()
    return folder


def current_path():
    return "/" + "/".join(cwd)


def resolve_path(path):
    if path.startswith("/"):
        result = []
    else:
        result = list(cwd)

    for piece in path.split("/"):
        if piece == "" or piece == ".":
            continue
        if piece == "..":
            if len(result) > 0:
                result.pop()
        else:
            result.append(piece)
    return result


def get_node(parts):
    node = vfs
    for name in parts:
        if type(node) != dict or name not in node:
            return None
        node = node[name]
    return node


def ls(args):
    if len(args) > 1:
        write("ls: слишком много аргументов")
        return False
    if len(args) == 0:
        target = "."
    else:
        target = args[0]

    node = get_node(resolve_path(target))
    if node is None:
        write("ls: нет такого файла или каталога: " + target)
        return False
    if type(node) == str:
        write(target)
        return True

    for name in sorted(node):
        if type(node[name]) == dict:
            write(name + "/")
        else:
            write(name)
    return True


def cd(args):
    global cwd
    if len(args) > 1:
        write("cd: слишком много аргументов")
        return False
    if len(args) == 0:
        cwd = []
        return True

    target = args[0]
    parts = resolve_path(target)
    node = get_node(parts)
    if node is None:
        write("cd: нет такого каталога: " + target)
        return False
    if type(node) == str:
        write("cd: это не каталог: " + target)
        return False

    cwd = parts
    return True


def mkdir(args):
    if len(args) == 0:
        write("mkdir: не указано имя каталога")
        return False
    if len(args) > 1:
        write("mkdir: слишком много аргументов")
        return False

    target = args[0]
    parts = resolve_path(target)
    if len(parts) == 0:
        write("mkdir: каталог уже существует: " + target)
        return False

    parent_parts = parts[:-1]
    folder_name = parts[-1]
    parent = get_node(parent_parts)
    if parent is None:
        write("mkdir: нет родительского каталога: " + target)
        return False
    if type(parent) == str:
        write("mkdir: родитель не является каталогом: " + target)
        return False
    if folder_name in parent:
        write("mkdir: объект уже существует: " + target)
        return False

    parent[folder_name] = {}
    return True


def echo(args):
    write(" ".join(args))
    return True


def head(args):
    count = 10
    if len(args) > 0 and args[0] == "-n":
        if len(args) < MIN_HEAD_ARGUMENTS:
            write("head: после -n нужно указать число")
            return False
        if not args[1].isdigit():
            write("head: после -n нужно указать число")
            return False
        count = int(args[1])
        args = args[2:]

    if len(args) == 0:
        write("head: не указан файл")
        return False
    if len(args) > 1:
        write("head: слишком много аргументов")
        return False

    target = args[0]
    node = get_node(resolve_path(target))
    if node is None:
        write("head: нет такого файла: " + target)
        return False
    if type(node) == dict:
        write("head: это каталог, а не файл: " + target)
        return False

    for line in node.splitlines()[:count]:
        write(line)
    return True


def expand_vars(text):
    result = ""
    position = 0
    while position < len(text):
        if text[position] == "$":
            position = position + 1
            name = ""
            while position < len(text):
                symbol = text[position]
                if not (symbol.isalnum() or symbol == "_"):
                    break
                name = name + symbol
                position = position + 1
            if name == "":
                result = result + "$"
            else:
                result = result + os.environ.get(name, "")
        else:
            result = result + text[position]
            position = position + 1
    return result


def parse(line):
    return expand_vars(line).split()


def run_command(parts):
    if len(parts) == 0:
        return True

    name = parts[0]
    args = parts[1:]
    if name == "ls":
        return ls(args)
    if name == "cd":
        return cd(args)
    if name == "mkdir":
        return mkdir(args)
    if name == "echo":
        return echo(args)
    if name == "head":
        return head(args)
    if name == "exit":
        if len(args) > 0:
            write("exit: команда не принимает аргументы")
            return False
        window.destroy()
        return True

    write(name + ": команда не найдена")
    return False


def on_enter(event):
    command = entry.get()
    entry.delete(0, "end")
    write(current_path() + "$ " + command)
    run_command(parse(command))


entry.bind("<Return>", on_enter)


def run_script(path):
    if not os.path.exists(path):
        write("Ошибка: файл скрипта не найден: " + path)
        return
    if not os.path.isfile(path):
        write("Ошибка: неверный формат скрипта, это не файл: " + path)
        return

    try:
        with open(path, encoding="utf-8") as file:
            lines = file.readlines()
    except (OSError, UnicodeDecodeError):
        write("Ошибка: не удалось прочитать скрипт: " + path)
        return

    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        write(current_path() + "$ " + line)
        parts = parse(line)
        success = run_command(parts)
        if not success:
            message = "[скрипт] ошибка в строке " + str(number)
            write(message + ", строка пропущена")
        if parts == ["exit"]:
            return


if params.vfs is None:
    vfs = {
        "readme.txt": "Это VFS по умолчанию\n",
        "home": {
            "user": {
                "notes.txt": "Мои заметки\n"
            }
        }
    }
    write("VFS не указана, создана VFS по умолчанию")
elif not os.path.exists(params.vfs):
    vfs = {}
    write("Ошибка загрузки VFS: путь не найден: " + params.vfs)
elif not os.path.isdir(params.vfs):
    vfs = {}
    message = "Ошибка загрузки VFS: неверный формат, это не папка: "
    write(message + params.vfs)
else:
    vfs = load_dir(params.vfs)
    write("VFS загружена из: " + params.vfs)

cwd = []

if params.script is not None:
    run_script(params.script)

window.mainloop()