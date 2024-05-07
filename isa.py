from enum import Enum


class OPCODE(str, Enum):

    ORG = "org"
    LD = "ld"
    ST = "st"

    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"

    CMP = "cmp"
    JMP = "jmp"
    JEQ = "jeq"
    JNE = "jne"

    LOOP = "loop"
    HLT = "hlt"

    def __str__(self) -> str:
        return str(self.value)


BRANCH_OPCODES = ["jmp", "jeq", "jne"]