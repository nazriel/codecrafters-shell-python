import os
import subprocess
import sys


class State:
    def __init__(self) -> None:
        self.cwd = os.getcwd()


state = State()
builtins = ["echo", "exit", "pwd", "type"]


def find_executable(executable):
    for p in os.environ["PATH"].split(":"):
        if os.path.exists(f"{p}/{executable}"):
            return f"{p}/{executable}"
    return None


def command_cd(args):
    def change_cwd(new_dir):
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            state.cwd = new_dir
            os.environ["PWD"] = state.cwd
            os.chdir(state.cwd)
            return True
        return False

    if len(args) == 0:
        return change_cwd(os.environ["HOME"])

    # TODO: handling of variables and quotes
    new_dir = " ".join(args).replace('"', "")
    if new_dir == "~":
        return change_cwd(os.environ["HOME"])

    if new_dir.startswith("/"):
        if not change_cwd(new_dir):
            sys.stdout.write(f"cd: {new_dir}: No such file or directory\n")
    else:
        new_path = state.cwd
        parts = new_dir.split("/")
        for p in parts:
            if p == "..":
                new_path = os.path.dirname(new_path).rstrip("/")
            elif p == ".":
                continue
            else:
                new_path = os.path.join(new_path, p).rstrip("/")

        if not change_cwd(new_path):
            sys.stdout.write(f"cd: {new_dir}: No such file or directory\n")


def command_echo(args):
    sys.stdout.write(" ".join(args) + "\n")


def command_exit(args):
    status_code = int(args[0]) if len(args) > 0 and args[0].isdigit() else 0
    sys.exit(status_code)


def command_pwd(args):
    sys.stdout.write(state.cwd + "\n")


def command_type(args):
    if args[0] in builtins:
        sys.stdout.write(f"{args[0]} is a shell builtin\n")
    else:
        exe = find_executable(args[0])
        if exe:
            sys.stdout.write(f"{args[0]} is {exe}\n")
        else:
            sys.stdout.write(f"{args[0]}: not found\n")


commands_map = {
    "cd": command_cd,
    "exit": command_exit,
    "echo": command_echo,
    "type": command_type,
    "pwd": command_pwd,
}


def handle_input(input):
    if input.strip() == "":
        return

    params = input.split(" ")
    if params[0] in commands_map:
        commands_map[params[0]](params[1:])
    else:
        exe = find_executable(params[0])
        if exe:
            subprocess.call([exe] + params[1:])
        else:
            sys.stdout.write(f"{params[0]}: command not found\n")


def print_prompt():
    sys.stdout.write("$ ")
    sys.stdout.flush()


def main():
    while True:
        print_prompt()
        last_input = input()
        handle_input(last_input)


if __name__ == "__main__":
    main()
