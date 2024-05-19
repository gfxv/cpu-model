from control_unit import Signal

    
class AddressDecoder:

    IO_MEMORY = 0x1

    @staticmethod
    def is_io(adderss: int) -> bool:
        if adderss < 0: 
            raise ValueError(f"Address `{adderss}` can't be negative")

        return adderss <= AddressDecoder.IO_MEMORY
    

class ALU:
    def __init__(self):
        # left: { ACC | PC }
        self.left = 0
        # right: { DR | CR }
        self.right = 0
        self.result = None
        self.status_n = False
        self.status_z = False

    def execute(self, signal: Signal):
        match signal:
            case Signal.SUM:
                return self.set_result(self.right + self.left)
            case Signal.MOD:
                return self.set_result(self.left % self.right)
            case Signal.INC:
                return self.set_result(self.left + 1)
            case Signal.CMP:
                return self.set_result(self.left - self.right)
            case _:
                print("Unknown signal: {}".format(signal))

                
    def set_result(self, result: int) -> dict:
        self.result = result
        self.status_n = True if result < 0 else False
        self.status_z = True if result == 0 else False


class DataPath:

    def __init__(self):
        self.acc = 0
        self.pc = 0
        self.dr = 0
        self.cr = 0
        self.ar = 0
        self.z = 0
        self.n = 0


