import json
import sys

from cpu import CPU


def main(args) -> None:
    program, input_data = load_input(args)
    cpu = CPU()
    cpu.load_program_to_memory(program, input_data)
    instructions, out, ticks = cpu.run()

    print(f"Instructions: {instructions}")
    print(f"Ticks: {ticks}")
    print("=== OUT ===")
    print("--- bytes ---")
    print(" ".join(list(map(str, out))))
    print("--- string ---")
    print("".join(list(map(lambda c: chr(c), out))))


def load_input(args) -> tuple:
    program = read_program(args[1])
    input_data = None
    if len(args) > 2 and args[2] != "":
        input_data = read_input(args[2])

    return program, input_data


def read_program(path) -> dict:
    with open(path, "r") as source:
        program = json.load(source)
        return program


def read_input(path) -> list:
    with open(path, "r") as file:
        data = list(map(lambda sym: ord(sym), list(file.read())))
        data[0] = int(chr(data[0]))
        return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Input file not found. \nusage: machine.py <input_program>")
    main(sys.argv)
