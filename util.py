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

def manhattanDistance(piece1, piece2):
	return (abs(piece1.pos[0]-piece2.pos[0]) + abs(piece1.pos[1] - piece2.pos[1])) 


def computeMinDistFromOtherPieces(piece, pieces):

	mindist = float('inf')

	for p in pieces:
		if p != piece and manhattanDistance(p, piece) < mindist:
			mindist = manhattanDistance(p, piece)

	return mindist
