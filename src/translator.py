# import json
import logging
import sys

import isa
from binary import Encoder

logging.basicConfig(
    level=logging.INFO, 
    format="%(levelname)s: %(message)s"
)


COMMENT_SYMBOL = ";"
START_LABEL = "_start"

def main(args: list[str]) -> None:
    _, source, target = args

    raw_lines = read_source_file(source)
    code = translate(raw_lines)

    bin_code = Encoder.to_binary(code)

    print(bin_code)

    write_target_file(target, bin_code)

    # write_target_file(target, code)


def read_source_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


def write_target_file(path: str, data) -> None:
    # json_object = json.dumps(data, indent=2)
    with open(path, "wb") as target:
        for inst in data:
            target.write(inst)


def translate(lines: list[str]) -> list[dict]:
    labels, code = parse_asm(lines)
    return substitute_labels(labels, code)


def get_meaningful_token(line: str) -> str:
    return line.split(COMMENT_SYMBOL, 1)[0].strip()


def parse_asm(lines: list[str]) -> tuple[dict, list]:
    labels = {}
    code = []

    for raw_line in lines:
        line = get_meaningful_token(raw_line)
        if len(line) == 0: 
            continue

        pc = len(code) + 1

        # handle labels `<label_name>:`
        if line.endswith(":"):
            label = line.strip(":")
            if label in labels: 
                logging.error(f"Redifination of label `{label}`")

            labels[label] = pc
            continue

        # handle `<instruction> <arg>`
        if " " in line:
            parts = line.split(" ")

            if len(parts) != 2:
                logging.error(f"Invalid instruction `{line}`")

            mnemonic, arg = parts
            opcode = isa.OPCODE(mnemonic)

            arg_type = "default"
            if "#" in arg:
                # raw = 'hardcoded' value
                # example: 
                #   ld #10 -- loads number 10 to acc
                #   ld 0x10 -- loads value at address 0x10
                arg_type = "raw" 
                arg = arg.strip("#")

            code.append({
                "index": pc,
                "opcode": opcode,
                "arg": arg,
                "arg_type": arg_type
            })

            continue

        # handle `<instruction>`
        opcode = isa.OPCODE(line)
        code.append({
            "index": pc,
            "opcode": opcode,
            "arg_type": "none",
            "arg": 0
        })

    return labels, code


def substitute_labels(labels: dict, code: list) -> list[dict]:
    start_label = labels[START_LABEL] if START_LABEL in labels else logging.error(f"`{START_LABEL}` label not found")

    for instruction in code:
        if "arg" in instruction and instruction["opcode"] in isa.BRANCH_OPCODES:
            label = instruction["arg"]
            if label not in labels:
                logging.error(f"Label `{label}` is not defined")
            instruction["arg"] = labels[label]

    # puts `jmp _start` at the beginning
    code.insert(0, {
        "index": 0,
        "opcode": "jmp",
        "arg": str(start_label),
        "arg_type": "init"
    })

    return code


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        logging.error("Wrong arguments: translator.py <source> <target>")
    main(sys.argv)