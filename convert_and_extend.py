def convert_and_extend(input_str: str, required_size: int):
        num = int(input_str)
        if num >= 0:
            binary_str = bin(num)[2:] 
        else:
            binary_str = bin((2**required_size)+num)[2:]
        if len(binary_str) < required_size:
            binary_str = '0' * (required_size - len(binary_str)) + binary_str
        return binary_str
input_string = "-16"
required_size = 8
result = convert_and_extend(input_string, required_size)
print(result)
