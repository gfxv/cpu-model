import json
import logging
import sys

import isa

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

COMMENT_SYMBOL = ";"
START_LABEL = "_start"


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

    org = 0
    offset = 0

    for raw_line in lines:
        line = get_meaningful_token(raw_line)
        if len(line) == 0:
            continue

        if isa.OPCODE.ORG in line:
            org = int(line.split(" ")[1])
            continue

        # +1 is needed to insert initial `jmp` at the position `0`
        # offset is needed to 'give space' for strings
        pc = len(code) + 1 + org + offset

        # handle labels `<label_name>:`
        if line.endswith(":"):
            label = line.strip(":")
            if label in labels:
                logging.error(f"Redifination of label `{label}`")

            labels[label] = pc
            continue

        # handle `<instruction> <arg>`
        if " " in line:
            parts = line.split(" ", 1)

            if len(parts) != 2:
                logging.error(f"Invalid instruction `{line}`")

            instruction = {}
            instruction["index"] = pc

            mnemonic, arg = parts
            opcode = isa.OPCODE(mnemonic)
            arg_type = "default"

            if opcode == isa.OPCODE.WORD:
                # word_size = 0
                # if '"' in arg:
                #     # handles `word "some text"`
                #     arg = arg.strip('"')
                #     word_size = len(arg)

                # else:
                #     # handles `word N` - allocates N cells
                #     buff_size = int(arg)
                #     arg = "-" * buff_size
                #     word_size = buff_size
                # arg_type = "word"
                # offset += word_size
                if '"' in arg:
                    string = reserve_string(arg.strip('"'), pc)
                    code += string
                    continue
                else:
                    buff_size = int(arg)
                    string = reserve_string("0" * buff_size, pc)
                    code += string
                    continue

            if "#" in arg or "&" in arg:
                arg_type = "raw"
                arg = arg.strip("#").strip("&")

            if "$" in arg:
                arg_type = "ptr"
                arg = arg.strip("$")

            if opcode == isa.OPCODE.INT:
                opcode = "nop"
                arg = int(arg)
                arg_type = "data"

            instruction["opcode"] = opcode
            instruction["arg"] = arg
            instruction["arg_type"] = arg_type

            code.append(instruction)
            continue

        # handle `<instruction>`
        opcode = isa.OPCODE(line)
        code.append({"index": pc, "opcode": opcode, "arg_type": "none", "arg": 0})

    return labels, code


def reserve_string(string: str, curr_index: int) -> list[dict]:
    filler_nops = []

    string_length = {
        "index": curr_index,
        "opcode": "nop",
        "arg": len(string),
        "arg_type": "data",
    }
    filler_nops.append(string_length)

    for s in range(len(string)):
        nop = {
            "index": s + curr_index + 1,  # +1 because of string length
            "opcode": "nop",
            "arg": ord(string[s]),
            "arg_type": "data",
        }
        filler_nops.append(nop)
    return filler_nops


def substitute_labels(labels: dict, code: list) -> list[dict]:
    start_label = (
        labels[START_LABEL]
        if START_LABEL in labels
        else logging.error(f"`{START_LABEL}` label not found")
    )

    for instruction in code:
        if instruction["arg"] in labels:
            label = instruction["arg"]
            if label not in labels:
                logging.error(f"Label `{label}` is not defined")
            instruction["arg"] = labels[label]

    # puts `jmp _start` at the beginning
    code.insert(
        0, {"index": 0, "opcode": "jmp", "arg": str(start_label), "arg_type": "default"}
    )

    return code


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Wrong arguments: translator.py <source> <target>")
    main(sys.argv)
