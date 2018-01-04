def collatz(number):
	if number %2 == 0:
		print (number //2)
		return number //2
	elif number %2 == 1:
		print (number *3 + 1)
		return number *3 + 1
a = int(input ('请输入一个数：'))
a1 = collatz (a)
while a1 != 1:
	collatz(a)
	
