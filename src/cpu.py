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

        MAX_VALUE = self.control_unit.data_path.MAX_INT
        for instruction in program:
            addr = instruction["index"]
            if int(instruction["arg"]) > MAX_VALUE:
                raise ValueError(
                    f"Operand can't be greater than {MAX_VALUE} \nindex: {addr}, instruction: {instruction["opcode"]}"
                )
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
