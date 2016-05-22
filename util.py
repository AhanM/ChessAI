# util.py
# --------
# Misc. Usefull tools

def isNotOutofBounds(x,y):
	return (x in range(0,8)) and (y in range(0,8))

def getIndexof(iterable, item):
	for i, el in enumerate(iterable):
		if el == item:
			return i
	return None

def raiseNotDefined():
	print "Error: Function not defined"
	