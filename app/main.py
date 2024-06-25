import os
import subprocess
import sys

builtins = ["exit", "echo", "type"]


def find_executable(executable):
    for p in os.environ["PATH"].split(":"):
        if os.path.exists(f"{p}/{executable}"):
            return f"{p}/{executable}"
    return None


def command_exit(args):
    status_code = int(args[0]) if len(args) > 0 and args[0].isdigit() else 0
    sys.exit(status_code)


def command_echo(args):
    sys.stdout.write(" ".join(args) + "\n")


def command_type(args):
    if args[0] in builtins:
        sys.stdout.write(f"{args[0]} is a shell builtin\n")
    else:
        exe = find_executable(args[0])
        if exe:
            sys.stdout.write(f"{args[0]} is {exe}\n")
        else:
            sys.stdout.write(f"{args[0]}: not found\n")


commands_map = {"exit": command_exit, "echo": command_echo, "type": command_type}


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
