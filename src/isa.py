from enum import Enum


class OPCODE(str, Enum):
    ORG = "org" # ? deprecated ?
    WORD = "word"
    INT = "int"
    LD = "ld"
    ST = "st"

    ADD = "add"
    SUB = "sub"
    MUL = "mul" # deprecated ?
    DIV = "div"
    MOD = "mod"
    INC = "inc"
    DEC = "dec"

    CMP = "cmp"
    JMP = "jmp"
    JEQ = "jeq" # depreacated ?
    JNE = "jne" # deprecated ?
    JZ = "jz"

    PUSH = "push"
    POP = "pop"

    # WRD = "word"
    HLT = "hlt"

    def __str__(self) -> str:
        return str(self.value)


BRANCH_OPCODES = ["jmp", "jeq", "jne", "jz"]
STACK_OPCODES = ["push", "pop"]
