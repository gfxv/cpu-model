import logging

from data_path import DataPath
from isa import BRANCH_OPCODES, OPCODE
from signals import Signal

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s | %(message)s")


class ControlUnit:
    def __init__(self, data_path: DataPath) -> None:
        self.data_path = data_path
        self._tick = 0
        self._instruction_counter = 0

    def tick(self):
        self._tick += 1

    def instr(self) -> None:
        self._instruction_counter += 1

    # Instruction Fetch
    def select_instruction(self):
        # PC -> AR
        self.data_path.sel_pc()
        self.data_path.alu.zero_right()
        self.data_path.alu.pass_value()
        self.data_path.latch_ar()
        self.tick()

        # MEM[AR] -> DR
        # PC + 1 -> PC
        self.data_path.latch_dr(Signal.READ_MEM)
        self.data_path.alu.execute(Signal.INC)
        self.data_path.latch_pc()
        self.tick()

        # DR -> CR
        self.data_path.latch_cr()
        self.tick()

    # Operand Fetch
    def select_operand(self):
        operand_type = self.data_path.cr["arg_type"]  # type: ignore
        if operand_type == "raw":
            # ARG -> DR
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_dr()
            self.tick()
            return
        if operand_type == "default":
            # CR.ARG -> AR
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            # MEM[AR] -> DR
            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()
            return

        if operand_type == "ptr":
            # ARG -> AR
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            # MEM[AR] -> DR
            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()

            # DR -> AR
            self.data_path.sel_data()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            # MEM[AR] -> DR
            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()
            return

        if operand_type == "none" or operand_type == "data":
            return

        raise ValueError(f"Unknown operand type: {operand_type}")

    def is_constrol_flow_instruction(self) -> bool:
        return self.data_path.cr["opcode"] in BRANCH_OPCODES

    def trace(self) -> None:
        instruction = self.data_path.cr
        arg = instruction["arg"] if instruction["arg_type"] != "none" else "-"
        trace = f"TICK: {self._tick:<4} | {instruction["opcode"]:<4} | ARG: {arg:<3} | TYPE: {instruction["arg_type"]:<7} | "
        trace += f"PC: {self.data_path.pc:<3} | ACC: {self.data_path.acc:<3} | DR: {self.data_path.dr["arg"]:<3} | AR: {self.data_path.ar:<3} | N: {str(self.data_path.n):<6} | Z: {str(self.data_path.z):<6}"
        logging.debug(trace)

    # Print Not-None memory cells
    def print_memory(self) -> None:
        for addr, value in enumerate(self.data_path.memory):
            if value is None:
                continue
            print(f"{addr}: {value}")

    # Run simulation
    def run(self):
        while True:
            self.instr()
            self.select_instruction()

            instruction = self.data_path.cr
            opcode = instruction["opcode"]

            if opcode == OPCODE.NOP:
                continue

            if self.is_constrol_flow_instruction():
                if opcode == OPCODE.JMP:
                    self.data_path.sel_cmd_operand()
                    self.data_path.alu.zero_left()
                    self.data_path.alu.pass_value()
                    self.data_path.latch_pc()
                    self.tick()
                    self.trace()
                    continue

                if opcode == OPCODE.JZ:
                    self.data_path.sel_cmd_operand()
                    self.data_path.alu.zero_left()
                    self.data_path.alu.pass_value()
                    if self.data_path.is_zero():
                        self.data_path.latch_pc()
                    self.tick()
                    self.trace()
                    continue

            self.select_operand()

            if opcode == OPCODE.HLT:
                self.tick()
                self.trace()
                raise SystemExit("=== HALT ===")

            if opcode == OPCODE.ADD:
                # ACC + DR -> ACC, NZ
                self.data_path.sel_acc()
                self.data_path.sel_data()
                self.data_path.alu.execute(Signal.SUM)
                self.data_path.latch_acc()
                self.data_path.latch_nz()
                self.tick()

            if opcode == OPCODE.INC:
                # ACC + 1 -> ACC, NZ
                self.data_path.sel_acc()
                self.data_path.alu.zero_right()
                self.data_path.alu.execute(Signal.INC)
                self.data_path.latch_acc()
                self.data_path.latch_nz()
                self.tick()

            if opcode == OPCODE.DEC:
                # ACC - 1 -> ACC, NZ
                self.data_path.sel_acc()
                self.data_path.alu.zero_right()
                self.data_path.alu.execute(Signal.DEC)
                self.data_path.latch_acc()
                self.data_path.latch_nz()
                self.tick()

            if opcode == OPCODE.LD:
                # DR -> ACC
                self.data_path.sel_data()
                self.data_path.alu.zero_left()
                self.data_path.alu.pass_value()
                self.data_path.latch_acc()
                self.tick()

            if opcode == OPCODE.ST:
                # DR -> AR
                self.data_path.sel_data()
                self.data_path.alu.zero_left()
                self.data_path.alu.pass_value()
                self.data_path.latch_ar()
                self.tick()

                # ACC -> DR
                self.data_path.sel_acc()
                self.data_path.alu.zero_right()
                self.data_path.alu.pass_value()
                self.data_path.latch_dr()
                self.tick()

                # DR -> MEM[AR]
                self.data_path.write_mem()
                self.tick()

            if opcode == OPCODE.CMP:
                # ACC - DR -> N, Z
                self.data_path.sel_data()
                self.data_path.sel_acc()
                self.data_path.alu.execute(Signal.SUB)
                self.data_path.latch_nz()
                self.tick()

            if opcode == OPCODE.MOD:
                # ACC % DR -> ACC, Z
                self.data_path.sel_data()
                self.data_path.sel_acc()
                self.data_path.alu.execute(Signal.MOD)
                self.data_path.latch_acc()
                self.data_path.latch_nz()
                self.tick()

            self.trace()
