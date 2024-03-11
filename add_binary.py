def add_binary (num1, num2):

    num1 = int(num1, 2)
    num2 = int(num2, 2)

    return bin(num1 + num2)[2:].zfill(32)

num1 = "1010"
num2 = "0010"

sum = add_binary(num1, num2)
print(sum)
