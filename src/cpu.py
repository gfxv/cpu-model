from control_unit import MICROCODE, ControlUnit, Signal
from data_path import ALU, AddressDecoder, DataPath
# from binary import Decoder

MEMORY_SIZE = 1024


class CPU:

    INSTRUCTION_LENGTH = 30

    def __init__(self, control_unit: ControlUnit, data_path: DataPath, alu: ALU):
        self.control_unit = control_unit
        self.data_path = data_path
        self.alu = alu
        self.microcode = MICROCODE
        self.mc_counter = 0
        self.memory = [None] * MEMORY_SIZE

    def load_programm_to_memory(instructions: list) -> None:
        pass

    def run(self) -> None:

        CPU_RUN = True
        while CPU_RUN:
            mc_instructions = self.microcode[self.mc_counter]
            for instruction in mc_instructions:
                
                # latch registers
                if instruction == Signal.LATCH_ACC: 
                    self.data_path.acc = self.alu.result
                if instruction == Signal.LATCH_AR: 
                    self.data_path.ar = self.alu.result
                if instruction == Signal.LATCH_PC: 
                    self.data_path.pc = self.alu.result
                if instruction == Signal.LATCH_CR: 
                    self.data_path.cr = self.alu.result

                # TODO: SOMETHING WITH `AddressDecoder`

                # read from memmory to dr
                if instruction == Signal.LATCH_DR and Signal.READ_MEM in mc_instructions:
                    if AddressDecoder.is_io(self.data_path.ar):
                       continue
                    self.data_path.dr = self.memory[self.data_path.ar]

                # write from dr to memory
                if instruction == Signal.LATCH_DR and Signal.WRITE_MEM in mc_instructions:
                    if AddressDecoder.is_io(self.data_path.ar):
                        continue
                    self.memory[self.data_path.ar] = self.data_path.dr

                # path value to left alu input
                if instruction == Signal.SEL_ACC: 
                    self.alu.left = self.data_path.acc
                if instruction == Signal.SEL_PC: 
                    self.alu.left = self.data_path.pc

                # path value to right alu input
                if instruction == Signal.SEL_DATA: 
                    self.alu.right = self.data_path.dr
                if instruction == Signal.SEL_CMD_OPERAND: 
                    self.alu.left = self.data_path.cr

                # stop 
                if instruction == Signal.HALT: 
                    CPU_RUN = False
                # start new command execution
                if instruction == Signal.TO_START: 
                    self.mc_counter = 0

            self.mc_counter += 1

    
    def print_trace(self) -> None:
        print("trace...")

            

    

