from control_unit import ControlUnit

class CPU:


    def __init__(self):
        self.control_unit = ControlUnit()

    def load_program_to_memory(self, program: list[dict], input_data: list = None) -> None:
        self.control_unit.data_path.input_buffer = input_data if input_data is not None else []
        for instruction in program:
            addr = instruction["index"]
            if instruction["arg_type"] == "word":
                self.control_unit.data_path.memory[addr] = len(instruction["arg"])
                for i in range(len(instruction["arg"])):
                    self.control_unit.data_path.memory[addr + i + 1] = ord(instruction["arg"][i])
                continue

            self.control_unit.data_path.memory[addr] = instruction

    def run(self) -> None:
        try:
            self.control_unit.run()
        except SystemExit:
            return self.result()

    def result(self) -> tuple:
        return self.control_unit.trace_list, self.control_unit.data_path.output_buffer

    def print_trace(self) -> None:
        print(f"TICK: {self.tick} |  | ACC: {self.data_path.acc} | PC: {self.data_path.pc} | DR: {self.data_path.dr} | CR: {self.data_path.cr} | AR: {self.data_path.ar}")
