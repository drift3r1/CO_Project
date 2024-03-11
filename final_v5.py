import re

def check_integer(s):
    pattern = r"[-+]?\d+"
    match = re.search(pattern, s)
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
    elif opcode in B_instructions:
        list2=list1[1].split(",")
        reg2=list2[1]
        reg1=list2[0]
        number=list2[2]

        
        if(number in Labels):
            a= Labels[number]
            b=PC-a

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
        if (register not in REGISTER_NAMES.keys()):
            return("a")
        immediate=list2[1]
        immediate = convert_and_extend(immediate, 21)
        immediate = immediate[::-1] # reversing the string to get MSB at index 0 and LSB at last index
        final_str = ""
        final_str += immediate[20] + immediate[10:0:-1] + immediate[11] + immediate[19:11:-1]
        final_str += REGISTER_NAMES[register]
        final_str += str(1101111)
        return final_str
    else:
        return("b")
pointer1 = open(r"C:\Users\atina\Downloads\CO Project evaluation framework\CO Project evaluation framework\automatedTesting\tests\assembly\simpleBin\test4.txt", "r")
# pointer1=open("xyz.txt","r")
# list1=pointer1.readlines()
# length=len(list1)
# pointer2=open("xyz1.txt","w")
list1 = pointer1.readlines()
desktop_path = r"C:\Users\atina\OneDrive\Desktop"
length=len(list1)
pointer2 = open(desktop_path + "\\open22.txt", "w")
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
