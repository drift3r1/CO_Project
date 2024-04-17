import re

def check_integer(s):
  pattern = r"^[-+]?\d+$"
  match = re.fullmatch(pattern, s)
  if match:
      return True
  else:
      return False
def convert_and_extend(input_str, required_size):
        num = int(input_str)
        if num >= 0:
            binary_str = bin(num)[2:] 
        else:
            binary_str = bin((2**required_size)+num)[2:]
        if len(binary_str) < required_size:
            binary_str = '0' * (required_size - len(binary_str)) + binary_str
        return binary_str
R_TYPE = "0110011"
R_instructions=["add","sub","sll","slt","sltu","xor","srl","or","and"]
B_TYPE = "1100011"
B_instructions=["beq","bne","blt","bge","bltu","bgeu"]
jal = "1101111"
lw="0000011"
addi="0010011"
sltiu="0010011"
jalr="1100111"
sw = "0100011"
lui = "0110111"
auipc="0010111"
REGISTER_NAMES = {
    'zero':"00000",'x0': "00000",
    'ra': "00001", 'x1': "00001",
    'sp': "00010", 'x2': "00010",  # Stack pointer register
    'gp': "00011", 'x3': "00011",
    'tp': "00100", 'x4': "00100",
    't0': "00101", 'x5': "00101",
    't1': "00110", 'x6': "00110",
    't2': "00111", 'x7': "00111",
    's0': "01000", 'x8': "01000",
    's1': "01001", 'x9': "01001",
    'a0': "01010", 'x10': "01010",
    'a1': "01011", 'x11': "01011",
    'a2': "01100", 'x12': "01100",
    'a3': "01101", 'x13': "01101",
    'a4': "01110", 'x14': "01110",
    'a5': "01111", 'x15': "01111",
    'a6': "10000", 'x16': "10000",
    'a7': "10001", 'x17': "10001",
    's2': "10010", 'x18': "10010",
    's3': "10011", 'x19': "10011",
    's4': "10100", 'x20': "10100",
    's5': "10101", 'x21': "10101",
    's6': "10110", 'x22': "10110",
    's7': "10111", 'x23': "10111",
    's8': "11000", 'x24': "11000",
    's9': "11001", 'x25': "11001",
    's10': "11010", 'x26': "11010",
    's11': "11011", 'x27': "11011",
    't3': "11100", 'x28': "11100",
    't4': "11101", 'x29': "11101",
    't5': "11110", 'x30': "11110",
    't6': "11111", 'x31': "11111"
}
def binary_string_output(string1):
    list1=string1.split()
    opcode=list1[0]
    if opcode == "sw":     
        l1=list1[1].split(",")
        opcodereq = sw
        func3 = "010"
        rs2 = l1[0]
        list2= l1[1].split("(")
        imm  = list2[0]
        rs1 = list2[1][0:-1]
        if rs1 in REGISTER_NAMES:
           rs1req = REGISTER_NAMES[rs1]
        else:
            return("a")
        if rs2 in REGISTER_NAMES:
           rs2req = REGISTER_NAMES[rs2]
        else:
            return("a")
        stringrequired = convert_and_extend(imm,12)
        

        return(stringrequired[0:7]+rs2req+rs1req+func3+stringrequired[7:]+opcodereq)
    elif opcode in ["lw","addi","sltiu","jalr"]:
            l1 = list1[1].split(",")
            if opcode == "lw":
                opcodereq = lw
                func3 = "010"
                rd = l1[0]
                list2= l1[1].split("(")
                imm  = list2[0]
                rs1 = list2[1][0:-1]
            elif opcode == "addi":
                opcodereq = addi
                func3 = "000"
                rd = l1[0]
                rs1 = l1[1]
                imm = l1[2]
            elif opcode == "sltiu":
                opcodereq = sltiu
                func3 = "011"
                rd = l1[0]
                rs1 = l1[1]
                imm = l1[2]
            elif opcode == "jalr":
                opcodereq = jalr
                func3 = "000"
                rd = l1[0]
                rs1 = l1[1]
                imm = l1[2]
            stringrequired = convert_and_extend(imm,12)
            if rs1 in REGISTER_NAMES:
                rs1req=REGISTER_NAMES[rs1]
            else:
                return("a")
            if rd in REGISTER_NAMES:
                rdreq=REGISTER_NAMES[rd]
            else:
                return("a")
            stringrequired = convert_and_extend(imm,12)
            return(stringrequired+rs1req+func3+rdreq+opcodereq)
    elif opcode in R_instructions:         
        if opcode == 'add':
            func3 = '000'
            func7="0000000"
        elif opcode == 'sub':
            func3 = '000'
            func7="0100000"
        elif opcode == 'sll':
            func3 = '001'
            func7="0000000"
        elif opcode == 'slt':
            func3 = '010'
            func7="0000000"
        elif opcode == 'sltu':
            func3 = '011'
            func7="0000000"
        elif opcode == 'xor':
            func3 = '100'
            func7="0000000"
        elif opcode == 'srl':
            func3 = '101'
            func7="0000000"
        elif opcode == 'or':
            func3 = '110'
            func7="0000000"
        elif opcode == 'and':
            func3 = '111'
            func7="0000000"
        list2=list1[1].split(",")
        rs1=list2[0]
        rs2=list2[1]
        rd=list2[2]
        if rs1 in REGISTER_NAMES:
            rs1req=REGISTER_NAMES[rs1]
        else:
            return("a")
        if rs2 in REGISTER_NAMES:
            rs2req=REGISTER_NAMES[rs2]
        else:
            return("a")
        if rd in REGISTER_NAMES:
            rdreq=REGISTER_NAMES[rd]
        else:
            return("a")
        bin_str = func7 + rdreq + rs2req + func3 + rs1req + R_TYPE
        return(bin_str)     
    elif opcode=="mul":
        list2=list1[1].split(",")
        rs1=list2[1]
        rs2=list2[2]
        rd=list2[0]
        rs1req=REGISTER_NAMES[rs1]
        rs2req=REGISTER_NAMES[rs2]
        rdreq=REGISTER_NAMES[rd]
        bin_str="0"*7 + rs2req+rs1req +"0"*3 +rdreq+"1"*7
        return(bin_str)
    elif opcode=="halt":
        return("0"*17+"010"+"0"*5+"1"*7)
    elif opcode=="rst":
        return("0"*17+"001"+"0"*5+"1"*7)
    elif opcode=="rvrs":
        list2=list1[1].split(",")
        rd=list2[0]
        rs1=list2[1]
        rs1req=REGISTER_NAMES[rs1]
        rdreq=REGISTER_NAMES[rd]
        return("0"*12+rs1req+"011"+rdreq+"1"*7)




    elif opcode in B_instructions:
        list2=list1[1].split(",")
        reg2=list2[1]
        reg1=list2[0]
        number=list2[2]

        
        if(number in Labels):
            a= Labels[number]
            b=a-PC

            imm = convert_and_extend(b,13)
        
        elif(number in  REGISTER_NAMES):
            imm = REGISTER_NAMES[number]
            imm  = (8*"0")+imm
        elif(check_integer(number)):
            imm  = convert_and_extend(number,13)
        else:
            return "c"
        if (reg2 not in REGISTER_NAMES.keys() or reg1 not in REGISTER_NAMES.keys()):
            return("a")
        func3 = ""
        if opcode == 'beq':
            func3 = '000'
        elif opcode == 'bne':
            func3 = '001'
        elif opcode == 'blt':
            func3 = '100'
        elif opcode == 'bge':
            func3 = '101'
        elif opcode == 'bltu':
            func3 = '110'
        elif opcode == 'bgeu':
            func3 = '111'
        final = ""
        imm = imm[::-1]
        final += imm[12] + imm[10:4:-1] + REGISTER_NAMES[reg2] + REGISTER_NAMES[reg1]+ func3+ imm[4:0:-1] + imm[11] + "1100011"
        return final
    elif opcode == "lui":
        list2 = list1[1].split(",")
        imm_val=list2[1]
        rs1=list2[0]
        imm_bin=convert_and_extend(imm_val,32)
        if rs1 in REGISTER_NAMES:
            rs1req=REGISTER_NAMES[rs1]
        else:
            return("a")
        bin_str =  imm_bin[0:20]+rs1req+"0110111"
        return bin_str
    elif opcode == "auipc":
        list2 = list1[1].split(",")
        rs1=list2[0]
        imm_val=list2[1]
        imm_bin=convert_and_extend(imm_val,32)
        if rs1 in REGISTER_NAMES:
            rs1req=REGISTER_NAMES[rs1]
        else:
            return("a")
        bin_str =  imm_bin[0:20]+rs1req+"0010111"
        return bin_str
    elif (opcode == "jal"):
        list2=list1[1].split(",")
        register=list2[0]
        number = list2[1]
        
        if (register not in REGISTER_NAMES.keys()):
            return("a")
        if(number in Labels):
            a= Labels[number]
            b=a-PC
            immediate = convert_and_extend(b,21)
        elif(check_integer(number)):
            immediate  = convert_and_extend(number,21)
        else:
            return "c"
        immediate = immediate[::-1] # reversing the string to get MSB at index 0 and LSB at last index
        final_str = ""
        final_str += immediate[20] + immediate[10:0:-1] + immediate[11] + immediate[19:11:-1]
        final_str += REGISTER_NAMES[register]
        final_str += str(1101111)
        return final_str
    else:
        return("b")
# Define the path to the file
desktop_path = r"C:\Users\atina\OneDrive\Desktop"
file_path = desktop_path + "\\open23.txt"

# Open the file in read mode
pointer1 = open(file_path, "r")

# Read the lines from the file
list1 = pointer1.readlines()

# Get the length of the list
length = len(list1)

# Open another file in write mode
pointer2 = open(desktop_path + "\\open24.txt", "w")


error=0
lengthofprogram=0
Labels={}
Labelswrong=[]
global PC
PC=0
for i in range(0,length):
    str3=list1[i]
    if str3.isspace()==True:
        continue
    elif ":" in str3:
        str4=str3
        str4.replace(" ","")
        if str4[len(str4)-2]==":":
            if str4[0:len(str4)-2] in Labels:
                Labelswrong.append(i)    
                lengthofprogram+=1
                continue
            else:
                Labels[str4[0:len(str4)-2]]=PC
                lengthofprogram+=1
                continue
        else:
            if ": " in str3:
                listtemp=str3.split(": ")
                if listtemp[0] in Labels:
                    Labelswrong.append(i)    
                    lengthofprogram+=1
                    continue
                else:
                    Labels[listtemp[0]]=PC
                    if len(listtemp)>1:
                        PC=PC+4
                        lengthofprogram+=1
            else:
                Labelswrong.append(i)    
                lengthofprogram+=1
    else:
        lengthofprogram+=1
        PC+=4
if lengthofprogram>64:
    pointer2.write("length of program exceeds 64 instructions\n")
if lengthofprogram<=64:
    for i in range(0,length-1):
        str1=list1[i]
        if i in Labelswrong:
            pointer2.write("error!!! label format wrong\n")
            pointer2.write(f"line number-{i+1}\n")
            error=error+1
            continue
        if str1.isspace()==True:
            continue
        if  ":" in str1:

            strtemp=str1
            strtemp.replace(" ","")
             
            if strtemp[len(strtemp)-2]==":":
                continue
            list12=str1.split(": ")
            str1new=list12[1]
            str4=str1new
            str5=str4.strip()
            if (str5=="beq zero,zero,0"or str5=="beq zero,zero,00000000"):
                    pointer2.write("error!!! virtual halt given early\n")
                    pointer2.write(f"line number-{i+1}\n")
                    error=error+1
            else:
                    str2=binary_string_output(str1new)
                    if str2=="a":
                        pointer2.write("error!!! no register found\n")
                        pointer2.write(f"line number-{i+1}\n")
                        error=error+1
                    elif str2=="b":
                        pointer2.write("error!!! no operand found\n")
                        pointer2.write(f"line number-{i+1}\n")
                        error=error+1
                    elif str2=="c":
                        pointer2.write("error!!! no label found\n")
                        pointer2.write(f"line number-{i+1}\n")
                        error=error+1
            continue
        str4=str1
        str5=str4.strip()
        if (str5=="beq zero,zero,0"or str5=="beq zero,zero,00000000"):
            pointer2.write("error!!! virtual halt given early\n")
            pointer2.write(f"line number-{i+1}\n")
            error=error+1
        else:
            str2=binary_string_output(str1)
            if str2=="a":
                pointer2.write("error!!! no register found\n")
                pointer2.write(f"line number-{i+1}\n")
                error=error+1
            elif str2=="b":
                pointer2.write("error!!! no operand found\n")
                pointer2.write(f"line number-{i+1}\n")
                error=error+1
            elif str2=="c":
                pointer2.write("error!!! no label found\n")
                pointer2.write(f"line number-{i+1}\n")
                error=error+1
if lengthofprogram<=64:    
    str1=list1[length-1]
    
    if (length-1) in Labelswrong:
        pointer2.write("error!!! wrong label \n")
        pointer2.write(f"line number-{length}\n")
        error=error+1
    
    elif ": " in str1:
        str2=str1
        list13=str2.split(": ")
        if len(list13)>1:
            str1new12=list13[1]
            str1new1=str1new12.strip()
            
            if str1new1 != "beq zero,zero,0" and str1new1 != "beq zero,zero,00000000":
                pointer2.write("error!!! Virtual Halt not given in code\n")
                pointer2.write(f"line number-{length}\n")
                error=error+1
        else:
            

            pointer2.write("error!!! Virtual Halt not given\n")
            pointer2.write(f"line number-{length}\n")

    elif str1.strip()!="beq zero,zero,0" and str1.strip()!= "beq zero,zero,00000000":
        print(str1)
        pointer2.write("error!!! Virtual Halt not given tonight\n")
        pointer2.write(f"line number-{length}\n")
        error=error+1
PC=0
if lengthofprogram<=64 and error==0:
    
    for i in range(0,length):
        str1=list1[i]
        # if str1.strip()=="halt":
        #     pointer2.write(0"*17+"010"+"0"*5+"1"*7 + "\n")
        #     break

        if str1.isspace()==True:
                continue
        elif ":" in str1:
            strtemp1=str1
            strtemp1.replace(" ","")
            listfinal=str1.split(": ")
            if strtemp1[len(strtemp1)-2]==":":
                continue
            else:
                listfinal=str1.split(": ")
                str2=binary_string_output(listfinal[1])
                pointer2.write(str2 + "\n")
                PC+=4
                continue
        else:
                str2=binary_string_output(str1)
                pointer2.write(str2 + "\n")
                PC+=4
pointer1.close()
pointer2.close()



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
Bonus_list = ["1111111"]
pc=0
Register_values = {
    "zero": 0, "ra": 0, "sp": 256, "gp": 0, "tp": 0, "t0": 0,
    "t1": 0,"t2": 0, "s0": 3, "s1": 2,"a0": 0,"a1": 0,
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
def Bonus_type(inputstr):
    global pc
    opcode = inputstr[-7:]
    func3  = inputstr[17:20]
    
    if(func3=="000"):
        rs2 = inputstr[7:12]
        rs1 = inputstr[12:17]
        rd = inputstr[20:25]
        rs2_name = get_register_name(rs2)
        rs1_name = get_register_name(rs1)
        rd_name = get_register_name(rd)
        Register_values[rd_name] = ignore_overflow(Register_values[rs1_name]*Register_values[rs2_name])
        pc+=4
        
    elif(func3 == "010"):
        pc = -1
    elif(func3=="001"):
        for key in Register_values.keys():
            if(key=="sp"):
                Register_values[key]= 256
            else:
                Register_values[key] = 0
        pc+=4
    elif(func3=="011"):
        rs1  = inputstr[12:17]
        rd = inputstr[20:25]
        rs1_name  = get_register_name(rs1)
        rd_name = get_register_name(rd)
        binary_rs1 = to_twos_complement(Register_values[rs1_name])
        reverese_rs1 = binary_rs1[len(binary_rs1)-1:1:-1]
        Register_values[rd_name] = convert(reverese_rs1)
        pc+=4
        

    
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
    elif(opcode in Bonus_list):
        Bonus_type(str)

def write_registers_to_file(file):
    global pc
    file.write(to_twos_complement(pc) + " ")
    for i in Register_values:
        file.write(to_twos_complement(Register_values[i]) + " ")
    file.write("\n")

def write_memory_to_file(file):
    for i in Memory_values:
        file.write(f"{integer_to_hex(i)}:{to_twos_complement(Memory_values[i])}\n")

desktop_path = r"C:\Users\atina\OneDrive\Desktop"
input_file = desktop_path + "\\open24.txt"
output_file = desktop_path + "\\open27.txt"

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
    if(pc!=-1):
        write_registers_to_file(file)
        write_memory_to_file(file)
