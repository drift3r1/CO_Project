import sys
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
def to_twos_complement(num):
    # Convert the number to binary and keep the last 32 bits
    binary = '0b'+format(num & 0xFFFFFFFF, '032b')

    # Return the binary representation
    return binary
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
def unsigned_binary(binary_string):
    # Extend binary_string to 32 bits
    extension_length = 32 - len(binary_string)
    if binary_string[0] == '1':  # If the number is negative
        binary_string = '1' * extension_length + binary_string
    else:  # If the number is positive
        binary_string = '0' * extension_length + binary_string
    return int(binary_string, 2)
def unsigned_integer(n):
    if(n>=0):
        return unsigned_binary(bin(n)[2:])
    else:
        return unsigned_binary(bin(n)[3:])
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
