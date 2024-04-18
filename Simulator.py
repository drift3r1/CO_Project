import sys
def to_twos_complement(num):
    # Convert the number to binary and keep the last 32 bits
    binary = '0b'+format(num & 0xFFFFFFFF, '032b')
    return binary

def unsigned_binary(binary_string):
    # Extend binary_string to 32 bits
    extension_length = 32 - len(binary_string)
    if binary_string[0] == '1':  # If the number is negative
        binary_string = '1' * extension_length + binary_string
    else:  # If the number is positive
        binary_string = '0' * extension_length + binary_string
    print(binary_string)
    return int(binary_string, 2)
def unsigned_integer(n):
    ans = to_twos_complement(n)
    return unsigned_binary(ans[2:])


Register_names = {
    "00000": 'zero', "00001": 'ra', "00010": 'sp', "00011": 'gp', "00100": 'tp', "00101": 't0', "00110": 't1', "00111": 't2',
    "01000": 's0', "01001": 's1', "01010": 'a0', "01011": 'a1', "01100": 'a2', "01101": 'a3',
    "01110": 'a4', "01111": 'a5', "10000": 'a6', "10001": 'a7', "10010": 's2', "10011": 's3',
    "10100": 's4', "10101": 's5', "10110": 's6', "10111": 's7', "11000": 's8', "11001": 's9',
    "11010": 's10', "11011": 's11', "11100": 't3', "11101": 't4', "11110": 't5', "11111": 't6'
}
# Rest of the code remains the same
R_list = ["0110011"]
I_list = ["0000011","0010011","0010011", "1100111"]
S_list = ["0100011"]
B_list = ["1100011"]
U_list = ["0110111","0010111"]
J_list = ["1101111"]
pc=0
Register_values = {
    "zero": 0, "ra": 0, "sp": 256, "gp": 0, "tp": 0, "t0": 0,
    "t1": 0,"t2": 0, "s0": 0, "s1": 0,"a0": 0,"a1": 0,
    "a2": 0,"a3": 0,"a4": 0,"a5": 0, "a6": 0,"a7": 0,
    "s2": 0,"s3": 0,"s4": 0,"s5": 0,"s6": 0, "s7": 0,
    "s8": 0,"s9": 0,"s10": 0, "s11": 0, "t3": 0,"t4": 0,
    "t5": 0,"t6": 0
}
def integer_to_hex(n):
    temp = hex(n)[2:].zfill(8)
    return '0x'+temp
def convert(binary_string):
    if binary_string[0] == '1':  # If the number is negative
        return -1 * (int(''.join('1' if b == '0' else '0' for b in binary_string), 2) + 1)
    else:  # If the number is positive
        return int(binary_string, 2)
def ignore_overflow(n):
    if(n< 2**31):
        return n
    num = to_twos_complement(n)
    ans = num[-32:]
    return convert(ans)

Memory_values={
    65536: 0, 65540: 0, 65544: 0, 65548: 0, 65552: 0, 
    65556: 0, 65560: 0, 65564: 0, 65568: 0, 65572: 0, 
    65576: 0, 65580: 0, 65584: 0, 65588: 0, 65592: 0, 
    65596: 0, 65600: 0, 65604: 0, 65608: 0, 65612: 0, 
    65616: 0, 65620: 0, 65624: 0, 65628: 0, 65632: 0, 
    65636: 0, 65640: 0, 65644: 0, 65648: 0, 65652: 0, 
    65656: 0, 65660: 0
}
def binary_to_int(binary_string):
    return int(binary_string, 2)
def get_register_name(register_code):
    return(Register_names[register_code])
def checkregvalidity(register_code):
    if register_code in Register_names:
        return(True)
    return(False)
#x0,gp and tp to always be kept as zero.....(should be implemented in print dictionary function)
R_instructions={"0000000":{"000":"add"},"0100000":{"000":"sub"},"0000000":{"001":"sll"},
                "0000000":{"010":"slt"},"0000000":{"011":"sltu"},"0000000":{"100":"xor"},
                "0000000":{"101":"srl"},"0000000":{"110":"or"},"0000000":{"111":"and"}}
def R_type(inputstr):
    global pc
    funct7 = inputstr[0:7]
    rs2 = inputstr[7:12]
    rs1 = inputstr[12:17]
    funct3 = inputstr[17:20]
    rd = inputstr[20:25]
    opcode = inputstr[25:32]
    rd_name = get_register_name(rd)
    rs1_name = get_register_name(rs1)
    rs2_name = get_register_name(rs2)
    if opcode == '0110011':  # R-type opcode
        if funct3 == '000':  # add or sub
            if funct7 == '0000000':  # add
                Register_values[rd_name] = Register_values[rs1_name] + Register_values[rs2_name]
                Register_values[rd_name] = ignore_overflow(Register_values[rd_name])
            elif funct7 == '0100000':  # sub
                Register_values[rd_name] = Register_values[rs1_name] - Register_values[rs2_name]
        elif funct3 == '001':  # sll
            Register_values[rd_name] = Register_values[rs1_name] << (Register_values[rs2_name] & 0x1F)
        elif funct3 == '010':  # slt
            Register_values[rd_name] = 1 if Register_values[rs1_name] < Register_values[rs2_name] else 0
        elif funct3 == '011':  # sltu
            Register_values[rd_name] = 1 if unsigned_integer(Register_values[rs1_name]) < unsigned_integer(Register_values[rs2_name]) else 0
        elif funct3 == '100':  # xor
            Register_values[rd_name] = Register_values[rs1_name] ^ Register_values[rs2_name]
        elif funct3 == '101':  # srl
            Register_values[rd_name] = Register_values[rs1_name] >> (Register_values[rs2_name] & 0x1F)
        elif funct3 == '110':  # or
            Register_values[rd_name] = Register_values[rs1_name] | Register_values[rs2_name]
        elif funct3 == '111':  # and
            Register_values[rd_name] = Register_values[rs1_name] & Register_values[rs2_name]
    pc += 4
def I_type(inputstr):
    global pc
    immediate = inputstr[0:12]
    rs1 = inputstr[12:17]
    func3 = inputstr[17:20]
    rd = inputstr[20:25]
    opcode = inputstr[-7:]
    rs1_name = get_register_name(rs1)
    rd_name = get_register_name(rd)
    rs_value = Register_values[rs1_name]
    if(func3=="010"):
        extended_imm = convert(immediate)
        Register_values[rd_name] = Memory_values[rs_value+extended_imm]
        pc=pc+4
    elif(func3=="000" and opcode == "0010011"):
        extended_imm = convert(immediate)
        Register_values[rd_name] = rs_value  + extended_imm
        pc+=4
    elif(func3=="011"):
        converted_imm = convert(immediate)
        
        if(unsigned_binary(immediate)>unsigned_integer(rs_value)):
            Register_values[rd_name] = 1
        pc+=4
    elif(func3=="000" and opcode=="1100111" ):
        if rd_name == "zero":
            pc = rs_value+convert(immediate)
            pc = pc & ~1
            return
        Register_values[rd_name]=pc+4
        pc = rs_value+convert(immediate)
        pc = pc & ~1
def S_type(inputstr):
    global pc
    immediate = inputstr[0:7] + inputstr[20:25]
    rs2 = inputstr[7:12]
    rs1  = inputstr[12:17]
    func3 = inputstr[17:20]
    opcode = inputstr[25:32]
    converted_imm = convert(immediate)
    rs1_name = get_register_name(rs1)
    rs2_name = get_register_name(rs2)
    rs1_value = Register_values[rs1_name]
    Memory_values[rs1_value+converted_imm] = Register_values[rs2_name]
    pc+=4
    
def B_type(inputstr):
    global pc
    imm =inputstr[0] + inputstr[24] + inputstr[1:7] + inputstr[20:24]+'0'
    rs2 = inputstr[7:12]
    rs1 = inputstr[12:17]
    func3 = inputstr[17:20]
    opcode = inputstr[25:32]
    converted_imm = convert(imm)
    rs1_name = get_register_name(rs1)
    rs2_name = get_register_name(rs2)
    rs1_value = Register_values[rs1_name]
    rs2_value = Register_values[rs2_name]

    if func3 == '000' and rs1_value == rs2_value:  # beq
        pc += converted_imm

    elif func3 == '001' and rs1_value != rs2_value:  # bne
        pc += converted_imm

    elif func3 == '100' and rs1_value < rs2_value:  # blt
        pc += converted_imm

    elif func3 == '101' and rs1_value >= rs2_value:  # bge
        pc += converted_imm

    elif func3 == '110' and unsigned_integer(rs1_value) < unsigned_integer(rs2_value):  # bltu
        pc += converted_imm

    elif func3 == '111' and unsigned_integer(rs1_value) >= unsigned_integer(rs2_value):  # bgeu
        pc += converted_imm

    else:
        pc += 4
        
def U_type(inputstr): 
    global pc
    imm = inputstr[0:20] +'000000000000'
    rd = inputstr[20:25]
    opcode = inputstr[25:32]
    converted_imm = convert(imm)
    rd_name = get_register_name(rd)
    if opcode == '0110111':  # lui
        Register_values[rd_name] = converted_imm
    elif opcode == '0010111':  # auipc
        Register_values[rd_name] = pc + converted_imm
    pc += 4

def J_type(inputstr):
    global pc
    imm = s[0] + s[12:20] + s[11]+ s[1:11]+ '0'
    rd = inputstr[20:25]
    opcode = inputstr[25:32]
    converted_imm = convert(imm)
    rd_name = get_register_name(rd)
    if opcode == '1101111':  # jal
        Register_values[rd_name] = pc + 4
        pc = pc + converted_imm
        pc = pc & ~1  # make the LSB=0

def solve(str):
    opcode =  str[-7:]
    if(opcode in R_list):
        R_type(str)
    elif(opcode in I_list):
        I_type(str)
    elif(opcode in S_list):
        S_type(str)
    elif(opcode in B_list):
        B_type(str)
    elif(opcode in U_list):
        U_type(str)
    elif(opcode in J_list):
        J_type(str)
def write_registers_to_file(file):
    global pc
    file.write(to_twos_complement(pc) + " ")
    for i in Register_values:
        file.write(to_twos_complement(Register_values[i]) + " ")
    file.write("\n")
def write_memory_to_file(file):
    for i in Memory_values:
        file.write(f"{integer_to_hex(i)}:{to_twos_complement(Memory_values[i])}\n")
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        list1 = [line.strip() for line in file]

    size = len(list1)
    index = 0

    with open(output_file, 'w') as file:
        while pc < size * 4 and list1[index] != "00000000000000000000000001100011":
            if list1[index] == "00000000000000000000000001100011":
                break
            a = pc
            if index < size:
                s = list1[index]
                solve(s)
                Register_values["zero"] = 0
                Register_values["gp"] = 0
                Register_values["tp"] = 0
                write_registers_to_file(file)
                index = pc // 4
            else:
                break
        write_registers_to_file(file)
        write_memory_to_file(file)