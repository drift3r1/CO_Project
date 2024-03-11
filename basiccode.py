import struct

# RISC-V instruction formats
R_TYPE = 0b0110011
I_TYPE = 0b0010011
S_TYPE = 0b0100011
B_TYPE = 0b1100011
U_TYPE = 0b0110111
J_TYPE = 0b1101111

# RISC-V opcodes
OP_LUI   = 0b0110111
OP_AUIPC = 0b0010111
OP_JAL   = 0b1101111
OP_JALR  = 0b1100111
OP_BRANCH = {
    'beq':  0b000,
    'bne':  0b001,
    'blt':  0b100,
    'bge':  0b101,
    'bltu': 0b110,
    'bgeu': 0b111
}
OP_LOAD = {
    'lb':  0b000,
    'lh':  0b001,
    'lw':  0b010,
    'lbu': 0b100,
    'lhu': 0b101
}
OP_STORE = {
    'sb': 0b000,
    'sh': 0b001,
    'sw': 0b010
}
OP_OP_IMM = {
    'addi':  0b000,
    'slti':  0b010,
    'sltiu': 0b011,
    'xori':  0b100,
    'ori':   0b110,
    'andi':  0b111
}
OP_OP = {
    'add':  0b0000000,
    'sub':  0b0100000,
    'sll':  0b0000000,
    'slt':  0b0000000,
    'sltu': 0b0000000,
    'xor':  0b0000000,
    'srl':  0b0000000,
    'sra':  0b0100000,
    'or':   0b0000000,
    'and':  0b0000000
}

# Register names and aliases
REGISTER_NAMES = {
    'zero': 0, 'x0': 0,
    'ra': 1, 'x1': 1,
    'sp': 2, 'x2': 2,  # Stack pointer register
    'gp': 3, 'x3': 3,
    'tp': 4, 'x4': 4,
    't0': 5, 'x5': 5,
    't1': 6, 'x6': 6,
    't2': 7, 'x7': 7,
    's0': 8, 'x8': 8,
    's1': 9, 'x9': 9,
    'a0': 10, 'x10': 10,
    'a1': 11, 'x11': 11,
    'a2': 12, 'x12': 12,
    'a3': 13, 'x13': 13,
    'a4': 14, 'x14': 14,
    'a5': 15, 'x15': 15,
    'a6': 16, 'x16': 16,
    'a7': 17, 'x17': 17,
    's2': 18, 'x18': 18,
    's3': 19, 'x19': 19,
    's4': 20, 'x20': 20,
    's5': 21, 'x21': 21,
    's6': 22, 'x22': 22,
    's7': 23, 'x23': 23,
    's8': 24, 'x24': 24,
    's9': 25, 'x25': 25,
    's10': 26, 'x26': 26,
    's11': 27, 'x27': 27,
    't3': 28, 'x28': 28,
    't4': 29, 'x29': 29,
    't5': 30, 'x30': 30,
    't6': 31, 'x31': 31
}

PC = 0  # Program counter
SP = None  # Stack pointer

labels = {}  # Dictionary to store labels and their addresses

def assemble(instruction):
    global PC, SP
    inst_parts = instruction.split()
    opcode = inst_parts[0]

    try:
        if opcode.endswith(':'):  # Label
            labels[opcode[:-1]] = PC
            return b''

        if opcode == 'lui':
            rd = REGISTER_NAMES[inst_parts[1]]
            imm = int(inst_parts[2], 16)
            binary = (U_TYPE << 26) | (imm & 0xFFFFF000) | (rd << 7)
        elif opcode == 'auipc':
            rd = REGISTER_NAMES[inst_parts[1]]
            imm = int(inst_parts[2], 16)
            binary = (U_TYPE << 26) | (imm & 0xFFFFF000) | (rd << 7)
        elif opcode == 'jal':
            rd = REGISTER_NAMES[inst_parts[1]]
            imm = labels[inst_parts[2]] - PC
            binary = (J_TYPE << 26) | (imm & 0x000FF000) | (rd << 7) | (imm & 0x00100000) >> 11 | (imm & 0x7FE00000) >> 20
        elif opcode == 'jalr':
            rd = REGISTER_NAMES[inst_parts[1]]
            rs1 = REGISTER_NAMES[inst_parts[2][1:]]
            imm = int(inst_parts[3], 16)
            binary = (I_TYPE << 26) | (imm & 0xFFF00000) >> 20 | (rs1 << 15) | (OP_JALR << 12) | (rd << 7) | (imm & 0x00000FF0) >> 4
        elif opcode in OP_BRANCH:
            rs1 = REGISTER_NAMES[inst_parts[1][1:]]
            rs2 = REGISTER_NAMES[inst_parts[2][1:]]
            imm = labels[inst_parts[3]] - PC
            binary = (B_TYPE << 26) | (OP_BRANCH[opcode] << 12) | (imm & 0x00000F00) >> 7 | (rs2 << 20) | (rs1 << 15) | (imm & 0x00000080) >> 4 | (imm & 0x7E000000) >> 20
        elif opcode in OP_LOAD:
            rd = REGISTER_NAMES[inst_parts[1]]
            rs1 = REGISTER_NAMES[inst_parts[2][1:]]
            imm = int(inst_parts[3], 16)
            binary = (I_TYPE << 26) | (OP_LOAD[opcode] << 12) | (imm & 0xFFF00000) >> 20 | (rs1 << 15) | (rd << 7) | (imm & 0x00000FF0) >> 4
        elif opcode in OP_STORE:
            rs1 = REGISTER_NAMES[inst_parts[1][1:]]
            rs2 = REGISTER_NAMES[inst_parts[2][1:]]
            imm = int(inst_parts[3], 16)
            binary = (S_TYPE << 26) | (OP_STORE[opcode] << 12) | (imm & 0xFE000000) >> 25 | (rs2 << 20) | (rs1 << 15) | (imm & 0x00000F80) >> 7
        elif opcode in OP_OP_IMM:
            rd = REGISTER_NAMES[inst_parts[1]]
            rs1 = REGISTER_NAMES[inst_parts[2][1:]]
            imm = int(inst_parts[3], 16)
            binary = (I_TYPE << 26) | (OP_OP_IMM[opcode] << 12) | (imm & 0xFFF00000) >> 20 | (rs1 << 15) | (rd << 7) | (imm & 0x00000FF0) >> 4
        elif opcode in OP_OP:
            rd = REGISTER_NAMES[inst_parts[1]]
            rs1 = REGISTER_NAMES[inst_parts[2][1:]]
            rs2 = REGISTER_NAMES[inst_parts[3][1:]]
            funct3 = 0b000
            funct7 = 0b0000000
            if opcode == 'sub':
                funct3 = 0b000
                funct7 = 0b0100000
            elif opcode == 'sll':
                funct3 = 0b001
                funct7 = 0b0000000
            elif opcode == 'slt':
                funct3 = 0b010
                funct7 = 0b0000000
            elif opcode == 'sltu':
                funct3 = 0b011
                funct7 = 0b0000000
            elif opcode == 'xor':
                funct3 = 0b100
                funct7 = 0b0000000
            elif opcode == 'srl':
                funct3 = 0b101
                funct7 = 0b0000000
            elif opcode == 'sra':
                funct3 = 0b101
                funct7 = 0b0100000
            elif opcode == 'or':
                funct3 = 0b110
                funct7 = 0b0000000
            elif opcode == 'and':
                funct3 = 0b111
                funct7 = 0b0000000

            binary = (R_TYPE << 26) | (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | (OP_OP[opcode])

        if opcode != 'j' and opcode != 'b':
            PC += 4

        return struct.pack('I', binary)

    except (KeyError, ValueError) as e:
        print(f"Error: {e}")
        return b'\x00\x00\x00\x00'

def main():
    global SP

    with open('input.txt', 'r') as input_file, open('output.bin', 'wb') as output_file:
        for line in input_file:
            instruction = line.strip()
            if instruction:
                binary = assemble(instruction)
                output_file.write(binary)

        # Set initial stack pointer
        SP = 0x7FFFFFF0
        output_file.seek(0)

        while True:
            instruction = input_file.readline().strip()
            if instruction == '':
                break
            if instruction.startswith('.'):
                if instruction == '.stack':
                    SP = int(input_file.readline().strip(), 16)
                else:
                    print(f"Unknown directive: {instruction}")
            else:
                binary = assemble(instruction)
                output_file.write(binary)

if _name_ == '_main_':
    main()
