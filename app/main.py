import sys


def handle_input(input):
    if input.strip() == "":
        return

    command = input.split(" ")
    sys.stdout.write(f"{command[0]}: command not found\n")


def print_prompt():
    sys.stdout.write("$ ")
    sys.stdout.flush()


def main():
    while True:
        print_prompt()
        last_input = input()
        if last_input == "exit":
            break

        handle_input(last_input)


if __name__ == "__main__":
    main()
