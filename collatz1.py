def collatz(number):
    if number %2 == 0:
        b = number // 2
        print (b)
        return b
    elif number %2 == 1:
        b = number *3 +1
        print (b)
        return b
try:
    a = int(input ('请输入一个整数：'))
except ValueError:
    a = int(input ('刚才输入的不是一个整数，请重新输入一个整数：'))
while True:
    a = collatz(a)
    if a == 1:
        break

