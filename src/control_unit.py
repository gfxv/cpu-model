from isa import OPCODE, BRANCH_OPCODES, STACK_OPCODES
from data_path import DataPath
from signals import Signal


class ControlUnit:

    def __init__(self, data_path: DataPath) -> None:
        self.data_path = data_path
        self._tick = 0

        self.trace_list = []

    def tick(self):
        self._tick += 1

    # Instruction Fetch
    def select_instruction(self):
        self.data_path.sel_pc()
        self.data_path.alu.zero_right()
        self.data_path.alu.pass_value()
        self.data_path.latch_ar()
        self.tick()

        self.data_path.latch_dr(Signal.READ_MEM)
        self.data_path.alu.execute(Signal.INC)
        self.tick()

        self.data_path.latch_cr()
        self.data_path.latch_pc()
        self.tick()

    # Operand Fetch
    def select_operand(self):
        operand_type = self.data_path.cr["arg_type"] # type: ignore
        if operand_type == "raw":
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_dr()
            self.tick()
            return
        if operand_type == "default":
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()
            return

        if operand_type == "ptr":
            self.data_path.sel_cmd_operand()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()

            self.data_path.sel_data()
            self.data_path.alu.zero_left()
            self.data_path.alu.pass_value()
            self.data_path.latch_ar()
            self.tick()

            self.data_path.latch_dr(Signal.READ_MEM)
            self.tick()
            return

        if operand_type == "none":
            return

        raise ValueError(f"Unknown operand type: {operand_type}")


    def is_constrol_flow_instruction(self) -> bool:
        return self.data_path.cr["opcode"] in BRANCH_OPCODES

    def is_stack_instruction(self) -> bool:
        return self.data_path.cr["opcode"] in STACK_OPCODES

    def trace(self) -> None:
        instruction = self.data_path.cr
        arg = instruction["arg"] if instruction["arg_type"] != "none" else "-"
        trace = f"TICK: {self._tick:<4} | {instruction["opcode"]:<4} | ARG: {arg:<3} | "
        trace += f"ACC: {self.data_path.acc:<3} | PC: {self.data_path.pc:<3} | AR: {self.data_path.ar:<3}"
        self.trace_list.append(trace)

    # Print Not-None memory cells
    def print_memory(self) -> None:
        for addr, value in enumerate(self.data_path.memory):
            if value is None:
                continue
            print(f"{addr}: {value}")

    # Run simulation
    def run(self):
        while True:
            self.select_instruction()

            instruction = self.data_path.cr
            opcode = instruction["opcode"]

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
                self.data_path.sel_data()
                self.data_path.sel_acc()
                self.data_path.alu.execute(Signal.MOD)
                self.data_path.latch_acc()
                self.data_path.latch_nz()
                self.tick()

            self.trace()
