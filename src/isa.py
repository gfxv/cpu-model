from enum import Enum


class OPCODE(str, Enum):
    ORG = "org"
    WORD = "word"
    INT = "int"
    LD = "ld"
    ST = "st"

    ADD = "add"
    SUB = "sub"
    MOD = "mod"
    INC = "inc"
    DEC = "dec"

    CMP = "cmp"
    JMP = "jmp"
    JZ = "jz"

    HLT = "hlt"

    def __str__(self) -> str:
        return str(self.value)


BRANCH_OPCODES = ["jmp", "jeq", "jne", "jz"]
STACK_OPCODES = ["push", "pop"]
