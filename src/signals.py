from enum import Enum, auto


class Signal(Enum):
    READ_MEM = auto()
    WRITE_MEM = auto()

    INC = auto()
    DEC = auto()
    SUM = auto()
    SUB = auto()
    MOD = auto()
