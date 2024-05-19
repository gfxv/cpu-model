from isa import OPCODE

# don't even ask how this works...

ADDR_LENGTH = 10
ARG_LENGTH = 12

OPCODE_BIN_MAP = {
    OPCODE.INC: "000001", # 0x1   
    OPCODE.ADD: "000010", # 0x2
    OPCODE.SUB: "000011", # 0x3
    OPCODE.MOD: "000100", # 0x4
    OPCODE.CMP: "000101", # 0x5
    OPCODE.JMP: "000110", # 0x6
    OPCODE.JEQ: "000111", # 0x7
    OPCODE.JZ : "001000", # 0x8
    OPCODE.LD : "001001", # 0x9
    OPCODE.ST : "001010", # 0xA
    OPCODE.HLT: "001011", # 0xB
}

ARG_TYPE_MAP = {
    "none": "00",
    "default": "01",
    "raw": "10",
    "init": "11"
}

class Encoder:

    # returns: 
    # <ADDR><COMMAND><ARG_TYPE><ARGUMENT>
    # ------------------------------
    # ADDR - 10b
    # COMMAND - 6b
    # ARG_TYPE - 2b
    # ARGUMENT - 12b
    # total: 30b

    @staticmethod
    def to_binary(code: list) -> str:
        result = []
        for instr in code:
            result.append(Encoder.encode(instr))

        return b"".join(result)

    @staticmethod
    def encode(instruction: dict) -> str:
        bits = Encoder.get_bits(instruction)
        # https://stackoverflow.com/questions/21220916/writing-bits-to-a-binary-file
        return int(bits[::-1], 2).to_bytes(4, 'little')
        
    @staticmethod
    def get_bits(instruction: dict) -> str:
        return Encoder.parse_addr(instruction) + Encoder.parse_command(instruction) + Encoder.parse_arg_type(instruction) + Encoder.parse_argument(instruction)

    @staticmethod
    def parse_addr(instruction) -> str:
        bin_str = bin(instruction["index"])
        raw_addr = list(bin_str.split("b")[1])
        return "".join(map(str, [0] * (ADDR_LENGTH - len(raw_addr)) + raw_addr))

    @staticmethod
    def parse_command(instruction) -> str:
        return OPCODE_BIN_MAP[instruction["opcode"]]

    @staticmethod    
    def parse_arg_type(instruction) -> list[int]:
        return ARG_TYPE_MAP[instruction["arg_type"]]

    @staticmethod
    def parse_argument(instruction) -> list[int]:
        bin_str = bin(int(instruction["arg"]))
        raw_arg = list(bin_str.split("b")[1])
        return "".join((map(str, [0] * (ARG_LENGTH - len(raw_arg)) + raw_arg)))


class Decoder:

    @staticmethod
    def decode(encoded) -> dict:
        raw_bytes = Decoder.parse_bytes(encoded)
        addr = Decoder.parse_addr(raw_bytes[:10])
        command = Decoder.parse_cmd(raw_bytes[10:16])
        arg_type = Decoder.parse_arg_type(raw_bytes[16:18])
        arg = Decoder.parse_argument(raw_bytes[18:])

        return {
            "index": addr,
            "opcode": str(command),
            "arg": arg,
            "arg_type": arg_type
        }

    @staticmethod
    def parse_bytes(str) -> str:
        # https://stackoverflow.com/questions/21220916/writing-bits-to-a-binary-file
        # (somewhere in the comments to the first solution)
        return format(int.from_bytes(str, "little"), "030b")[::-1]

    @staticmethod
    def parse_addr(raw_addr) -> int:
        return int(raw_addr, 2)

    @staticmethod
    def parse_cmd(raw_command) -> int:
        return list(OPCODE_BIN_MAP.keys())[list(OPCODE_BIN_MAP.values()).index(raw_command)]
    
    @staticmethod
    def parse_arg_type(raw_arg_type) -> str:
        return list(ARG_TYPE_MAP.keys())[list(ARG_TYPE_MAP.values()).index(raw_arg_type)]

    def parse_argument(raw_arg) -> str: 
        return str(int(raw_arg, 2))


# print("Instruction sample:\n", test_instr)
# print("Encoded: ")
# enc_bits = Encoder.get_bits(test_instr)
# encoded = Encoder.encode(test_instr)
# print(" - bits:", enc_bits)
# print(" - final bin:", encoded)

# dec_bits = Decoder.parse_bytes(encoded)
# decoded = Decoder.decode(encoded)
# print("Decoded: ")
# print(" - bits:", dec_bits)
# print(" - decoded instr:", decoded)










