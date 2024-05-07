import sys
import logging
import json

import isa


logging.basicConfig(
    level=logging.INFO, 
    format="%(levelname)s: %(message)s"
)


COMMENT_SYMBOL = ";"

def main(args: list[str]) -> None:
    _, source, target = args

    raw_lines = read_source_file(source)
    code = translate(raw_lines)

    write_target_file(target, code)


def read_source_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


def write_target_file(path: str, data) -> None:
    json_object = json.dumps(data, indent=2)
    with open(path, "w", encoding="utf-8") as target:
        target.write(json_object)


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
        if len(line) == 0: continue

        pc = len(code)

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

            code.append({
                "index": pc,
                "opcode": opcode,
                "arg": arg
            })

            continue

        # handle `<instruction>`
        opcode = isa.OPCODE(line)
        code.append({
            "index": pc,
            "opcode": opcode
        })

    return labels, code


def substitute_labels(labels: dict, code: list) -> list[dict]:
    for instruction in code:
        if "arg" in instruction and instruction["opcode"] in isa.BRANCH_OPCODES:
            label = instruction["arg"]
            if label not in labels:
                logging.error(f"Label `{label}` is not defined")
            instruction["arg"] = labels[label]

    return code



if __name__ == "__main__":
    if len(sys.argv) != 3: logging.error("Wrong arguments: translator.py <source> <target>")
    main(sys.argv)