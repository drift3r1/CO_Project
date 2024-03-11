num1 = 0b101  
num2 = 0b110100  
bin_num1 = bin(num1)[2:]
bin_num2 = bin(num2)[2:]
max_length = max(len(bin_num1), len(bin_num2))
bin_num1 = bin_num1.zfill(max_length)
bin_num2 = bin_num2.zfill(max_length)
print(bin_num1)
print(bin_num2)
