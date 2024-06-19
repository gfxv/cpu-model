import sys

from control_unit import ControlUnit
from data_path import DataPath


class CPU:
    def __init__(self):
        self.control_unit = ControlUnit(DataPath())

    def load_program_to_memory(
        self, program: list[dict], input_data: list = None
    ) -> None:
        self.control_unit.data_path.input_buffer = (
            input_data if input_data is not None else []
        )
        for instruction in program:
            addr = instruction["index"]
            # if instruction["arg_type"] == "word":
            #     self.control_unit.data_path.memory[addr] = len(instruction["arg"])
            #     for i in range(len(instruction["arg"])):
            #         self.control_unit.data_path.memory[addr + i + 1] = ord(
            #             instruction["arg"][i]
            #         )
            #     continue
            # if instruction["arg_type"] == "int":
            #     self.control_unit.data_path.memory[addr] = int(instruction["arg"])
            #     continue

            self.control_unit.data_path.memory[addr] = instruction

    def run(self):
        try:
            self.control_unit.run()
        except BufferError as e:
            print(str(e))
            print("Terminating...")
            sys.exit(0)
        except SystemExit:
            return self.result()

    def result(self) -> tuple:
        return (
            self.control_unit._instruction_counter,
            self.control_unit.data_path.output_buffer,
            self.control_unit._tick,
        )
