import logging

from signals import Signal


class AddressDecoder:
    IO_MEMORY = 0x1

    @staticmethod
    def is_io(address: int) -> bool:
        if int(address) < 0:
            raise ValueError(f"Address `{address}` can't be negative")
        if int(address) > DataPath.MEMORY_SIZE:
            raise ValueError(
                f"Address `{address}` can't be greater than {DataPath.MEMORY_SIZE}"
            )

        return int(address) == AddressDecoder.IO_MEMORY


class ALU:
    def __init__(self):
        # left: { ACC | PC }
        self.left = None
        # right: { DR | CR }
        self.right = None
        self.value = None
        self.status_n = False
        self.status_z = False

    def execute(self, signal: Signal):
        match signal:
            case Signal.SUM:
                self.set_result(int(self.right) + int(self.left))
            case Signal.SUB:
                self.set_result(int(self.left) - int(self.right))
            case Signal.MOD:
                self.set_result(int(self.left) % int(self.right))
            case Signal.INC:
                self.set_result(int(self.left) + 1)
            case Signal.DEC:
                self.set_result(int(self.left) - 1)
            case _:
                print("Unknown signal: {}".format(signal))

    def zero_left(self):
        self.left = 0

    def zero_right(self):
        self.right = 0

    def pass_value(self):
        result = self.left if self.right == 0 else self.right
        self.value = result

    def set_result(self, value: int):
        self.value = value
        self.status_n = True if value < 0 else False
        self.status_z = True if value == 0 else False


class DataPath:
    MEMORY_SIZE = 1024
    MAX_BUFFER_SIZE = 256

    def __init__(self):
        self.alu = ALU()
        self.acc = 0
        self.pc = 0
        self.dr = None
        self.cr = None
        self.ar = 0
        self.z = False
        self.n = False
        self.input_buffer = []
        self.output_buffer = []
        self.memory = [None] * DataPath.MEMORY_SIZE

    def read_mem(self):
        if AddressDecoder.is_io(self.ar):
            if len(self.input_buffer) == 0:
                raise BufferError("Input buffer is empty!")
            symbol = self.input_buffer.pop(0)
            self.dr["arg"] = symbol
            logging.info(f"IN: {symbol}")
            return
        self.dr = self.memory[int(self.ar)].copy()

    def write_mem(self):
        if AddressDecoder.is_io(self.ar):
            if len(self.output_buffer) >= DataPath.MAX_BUFFER_SIZE:
                raise BufferError("Output buffer overflow!")
            self.output_buffer.append(self.dr["arg"])
            logging.info(f"OUT: {self.dr["arg"]}")
            return
        self.memory[int(self.ar)] = self.dr

    def sel_acc(self):
        self.alu.left = self.acc

    def sel_pc(self):
        self.alu.left = self.pc

    def sel_data(self):
        self.alu.right = self.dr["arg"]

    def sel_cmd_operand(self):
        self.alu.right = self.cr["arg"]

    def latch_pc(self):
        self.pc = self.alu.value

    def latch_acc(self):
        self.acc = self.alu.value

    def latch_dr(self, signal=None):
        if signal is None:
            self.dr["arg"] = self.alu.value
            return
        self.read_mem()

    def latch_cr(self):
        self.cr = self.dr.copy()

    def latch_ar(self):
        self.ar = self.alu.value

    def latch_nz(self):
        self.n = self.alu.status_n
        self.z = self.alu.status_z

    def is_zero(self) -> bool:
        return self.z

    def is_negative(self) -> bool:
        return self.n

    def _print_cell(self) -> None:
        print(f"[{self.ar}] {self.memory[int(self.ar)]}")

    def _print_commad(self) -> None:
        print(f"{self.cr["opcode"]} {self.cr["arg"]} ({self.cr["arg_type"]})")
