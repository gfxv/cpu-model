from enum import Enum


class OPCODE(str, Enum):
    ORG = "org" # ? deprecated ?
    LD = "ld"
    ST = "st"

    ADD = "add"
    SUB = "sub"
    MUL = "mul" # deprecated ?
    DIV = "div"
    MOD = "mod"
    INC = "inc"

    CMP = "cmp"
    JMP = "jmp"
    JEQ = "jeq" # depreacated ?
    JNE = "jne" # deprecated ?
    JZ = "jz"

    LOOP = "loop" # deprecated
    HLT = "hlt"

    def __str__(self) -> str:
        return str(self.value)


BRANCH_OPCODES = ["jmp", "jeq", "jne", "jz"]
