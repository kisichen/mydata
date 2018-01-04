aa = {'gold coin':44,'rope':1}
add = ['gold coin','dagger','gold coin','gold coin','ruby']

def addinventory (inventory,items):
	for i in items:
		if i in inventory.keys():
			inventory[i]=inventory[i]+1
		else:
			inventory[i]=1

def printinventory(totalnumber):
	addinventory(aa,add)
	total = 0
	for a,b in totalnumber.items():
		print (str(b).ljust(8)+a)
		total +=b
	print ('所有物品的总和为： '+ str(total))
print('原商品数据')
print (aa)
print ('需要添加的商品')
print (add)
print ('添加完后商品的个数级总和')
printinventory (aa)