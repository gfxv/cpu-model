from enum import Enum, auto

from isa import OPCODE


microcode_addr = int

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
    SUM = auto()
    MOD = auto()
    CMP = auto()

    CMD_OPERAND = auto()
    TO_START = auto()
    HALT = auto()
    


MICROCODE = [
    # <<< INSTRUCTION FETCH >>>
    # MEM[PC] -> DR
    [Signal.SEL_PC, Signal.LATCH_AR, Signal.READ_MEM, Signal.LATCH_DR], # 0
    # PC -> ACC; 
    # ACC + 1 -> PC; 
    # DR -> CR
    [Signal.SEL_PC, Signal.INC, Signal.LATCH_PC, Signal.LATCH_CR], # 1

    # <<< OPERAND FETCH >>>
    # MEM[...CR] -> DR
    [Signal.SEL_CMD_OPERAND, Signal.CMD_OPERAND, Signal.LATCH_AR, Signal.READ_MEM, Signal.LATCH_DR], # 2

    # <<< OPERAND FETCH >>>
    # MEM[DR] -> DR
    [Signal.SEL_DATA, Signal.LATCH_AR, Signal.READ_MEM, Signal.LATCH_DR], # 3

    # <<< EXECUTION >>>
    # < LD >
    # DR -> ACC
    [Signal.SEL_DATA, Signal.LATCH_ACC, Signal.TO_START] # 4
    
    # < ST >
    # ACC -> MEM[DR]
    [Signal.SEL_DATA, Signal.LATCH_AR, Signal.SEL_ACC, Signal.LATCH_DR, Signal.WRITE_MEM, Signal.TO_START], # 5

    # < ADD >
    # ACC + DR -> ACC
    [Signal.SEL_ACC, Signal.SEL_DATA, Signal.SUM, Signal.LATCH_ACC, Signal.LATCH_NZ, Signal.TO_START], # 6

    # < MOD >
    # ACC % DR -> ACC
    [Signal.SEL_ACC, Signal.SEL_DATA, Signal.MOD, Signal.LATCH_ACC, Signal.TO_START] # 7

    # < INC >
    # ACC + 1 -> ACC
    [Signal.SEL_ACC, Signal.INC, Signal.LATCH_ACC] # 8

    # < HALT >
    [Signal.HALT, Signal.TO_START]

]


# in progress...
class ControlUnit:

    @staticmethod
    def opcode_to_mc(opcode) -> microcode_addr:
        match opcode:
            case OPCODE.ADD:
                return 10
            # and so on...