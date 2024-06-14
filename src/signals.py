from enum import Enum, auto

class Signal(Enum):

    LATCH_ACC = auto()
    LATCH_AR = auto()
    LATCH_PC = auto()
    LATCH_DR = auto()
    LATCH_CR = auto()
    LATCH_NZ = auto()

    READ_MEM = auto()
    WRITE_MEM = auto()

    SEL_ACC = auto()
    SEL_PC = auto()
    SEL_DATA = auto()
    SEL_CMD_OPERAND = auto()

    # TODO: add ALU signals
    INC = auto()
    DEC = auto()
    SUM = auto()
    SUB = auto()
    MOD = auto()
    CMP = auto()
