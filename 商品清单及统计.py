aa={'rop':1,'torch':6,'gold coin':42,'dagger':1,'arrow':12}
def displayaa(inventory):
	total = 0
	for a,b in inventory.items():
		print (str(b)+'  '+a)
		total += b
	print ('所有的库存一共是： '+str(total) + '个')
displayaa(aa)