import util
from action import Action

class Piece(object):
	"""
	Piece object shall help represent properties of chess pieces on the board
	Properties shall most definitely include:
		- Position
		- Color
		- 
	Functions should be:
		- valid moves
		- attacks / captures
		- String Representation
	"""
	def __init__(self, color, (x,y), index):
		super(Piece, self).__init__()
		self.color = color
		self.pos = self.x, self.y = x,y
		self.index = index

	
	def validMoves(self, config):
		moves = []

		return moves

	def toString(self):

		return "X"

class Pawn(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 1

	def toString(self):
		return "P"

	def validMoves(self, config):
		valid_moves = []
		x,y = self.pos
		
		self.player_pieces_pos = config.getPlayerPositions(self.color)
		self.enemy_pieces_pos = config.getEnemyPositions(self.color)

		if self.color == "White":
			# moving pawn one tile in front
			if util.isNotOutofBounds(x,y+1):
				valid_moves.append((x,y+1)) 
			# moving pawn two tiles in front
			if y == 1:
				valid_moves.append((x,y+2))

			# Attacking diagonally 1 -> Normal Attack

			# Attacking diagonally 2 -> When opponent pawn moves two in front

		else:
			# moving pawn one tile in front
			if util.isNotOutofBounds(x,y-1):
					valid_moves.append((x,y-1))

			# moving pawn two tiles in front
			if y == 6:
				if (x,y-1) not in self.player_pieces_pos+self.enemy_pieces_pos:
					valid_moves.append((x,y-2))

			# Attacking diagonally 1 -> Normal Attack

			# Attacking diagonally 2 -> When opponent pawn moves two in front

		# Pawn Promotion?

		for (newx,newy) in valid_moves:
			# Check for collisions
			action = Action(self, (newx,newy), config)
			if not action.isValid(): valid_moves.remove((newx,newy))

		return valid_moves

class Knight(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 3

	def toString(self):
		return "N"

	def validMoves(self, config):
		self.player_pieces_pos = config.getPlayerPositions(self.color)
		self.enemy_pieces_pos = config.getEnemyPositions(self.color)

		valid_moves = []
		x,y = self.pos
		# +2, +1 | +2, -1 | -2 + 1 | -2, -1 | +1,+2 | +1, -2| -1, +2| -1,-2
		incx = 1
		incy = 2
		
		for i in range(4):
			for j in range(2):
				if util.isNotOutofBounds(x+incx, y+incy):
					valid_moves.append((x+incx, y+incy))
				incx = -1 * incx
			incy = -1 * incy

			if i == 1: incx, incy = incy, incx

		# Check for collisions
		for (newx,newy) in valid_moves:
			action = Action(self, (newx,newy), config)
			if not action.isValid(): valid_moves.remove((newx,newy))

		return valid_moves

class Bishop(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 3

	def toString(self):
		return "B"

	def validMoves(self, config):
		self.player_pieces_pos = config.getPlayerPositions(self.color)
		self.enemy_pieces_pos = config.getEnemyPositions(self.color)

		x,y = self.pos
		valid_moves = []

		# left bottom - right top diagonal
		for i in range(8):
			if util.isNotOutofBounds(x+i, y+i):
				# restricting movement because of other player pieces
				if (x+i,y+i) in self.player_pieces_pos:
					break
				valid_moves.append((x+i,y+i))
				# restricting movement because of enemy pieces
				if (x+i,y+i) in self.enemy_pieces_pos:
					break

		for i in range(8):
			if util.isNotOutofBounds(x-i, y-i):
				# restricting movement because of other player pieces
				if (x-i,y-i) in self.player_pieces_pos:
					break
				valid_moves.append((x-i, y-i))
				# restricting movement because of enemy pieces
				if (x+i,y+i) in self.enemy_pieces_pos:
					break				

		# right botom - left top diagonal
		for i in range(8):
			if util.isNotOutofBounds(x-i, y+i):
				# restricting movement because of other player pieces
				if (x-i,y+i) in self.player_pieces_pos:
					break
				valid_moves.append((x-i,y+i))
				# restricting movement because of enemy pieces
				if (x-i,y+i) in self.enemy_pieces_pos:
					break

		for i in range(8):
			if util.isNotOutofBounds(x+i, y-i):
				# restricting movement because of other player pieces
				if (x+i,y-i) in self.player_pieces_pos:
					break
				valid_moves.append((x+i, y-i))
				# restricting movement because of enemy pieces
				if (x+i,y-i) in self.enemy_pieces_pos:
					break

		for (x,y) in valid_moves:
			# Check for collisions
			action = Action(self, (x,y), config)
			if not action.isValid(): valid_moves.remove((x,y))

		return valid_moves

class Rook(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 5

	def toString(self):
		return "R"

	def validMoves(self, config):
		self.player_pieces_pos = config.getPlayerPositions(self.color)
		self.enemy_pieces_pos = config.getEnemyPositions(self.color)

		x,y = self.pos
		valid_moves = []

		# same row 
		for i in range(x-1,0,-1):
			# restricting movement because of other player pieces
			if (i,y) in self.player_pieces_pos:
				break
			valid_moves.append((i,y))

			# restricting movement because of enemy pieces
			if (i,y) in self.enemy_pieces_pos:
				break

		for i in range(x+1,8):
			# restricting movement because of other player pieces
			if (i,y) in self.player_pieces_pos+self.enemy_pieces_pos:
				break
			valid_moves.append((i,y))

			# restricting movement because of enemy pieces
			if (i,y) in self.enemy_pieces_pos:
				break

		# same column 
		for i in range(y-1,0,-1):
			# restricting movement because of other player pieces
			if (x,i) in self.player_pieces_pos:
				break
			valid_moves.append((x,i))

			# restricting movement because of enemy pieces
			if (x,i) in self.enemy_pieces_pos:
				break

		for i in range(y+1,8):
			# restricting movement because of other pieces
			if (x,i) in self.player_pieces_pos+self.enemy_pieces_pos:
				break
			valid_moves.append((x,i))

			# restricting movement because of enemy pieces
			if (x,i) in self.enemy_pieces_pos:
				break

		# for (x,y) in valid_moves:
		# 	# Check for collisions
		# 	action = Action(self, (x,y), self.player_pieces, self.enemy_pieces)
		# 	if not action.isValid(): valid_moves.remove((x,y))

		return valid_moves

class Queen(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 9

	def toString(self):
		return "Q"

	def validMoves(self, config):
		valid_moves = []
		x,y = self.pos

		self.player_pieces_pos = config.getPlayerPositions(self.color)
		self.enemy_pieces_pos = config.getEnemyPositions(self.color)

		# same row 
		for i in range(x-1,0,-1):
			# restricting movement because of other player pieces
			if (i,y) in self.player_pieces_pos:
				break
			valid_moves.append((i,y))

			# restricting movement because of enemy pieces
			if (i,y) in self.enemy_pieces_pos:
				break

		for i in range(x+1,8):
			# restricting movement because of other player pieces
			if (i,y) in self.player_pieces_pos+self.enemy_pieces_pos:
				break
			valid_moves.append((i,y))

			# restricting movement because of enemy pieces
			if (i,y) in self.enemy_pieces_pos:
				break

		# same column 
		for i in range(y-1,0,-1):
			# restricting movement because of other player pieces
			if (x,i) in self.player_pieces_pos:
				break
			valid_moves.append((x,i))

			# restricting movement because of enemy pieces
			if (x,i) in self.enemy_pieces_pos:
				break

		for i in range(y+1,8):
			# restricting movement because of other pieces
			if (x,i) in self.player_pieces_pos+self.enemy_pieces_pos:
				break
			valid_moves.append((x,i))

			# restricting movement because of enemy pieces
			if (x,i) in self.enemy_pieces_pos:
				break

		# left bottom - right top diagonal
		for i in range(8):
			if util.isNotOutofBounds(x+i, y+i):
				# restricting movement because of other player pieces
				if (x+i,y+i) in self.player_pieces_pos:
					break
				valid_moves.append((x+i,y+i))
				# restricting movement because of enemy pieces
				if (x+i,y+i) in self.enemy_pieces_pos:
					break

		for i in range(8):
			if util.isNotOutofBounds(x-i, y-i):
				# restricting movement because of other player pieces
				if (x-i,y-i) in self.player_pieces_pos:
					break
				valid_moves.append((x-i, y-i))
				# restricting movement because of enemy pieces
				if (x+i,y+i) in self.enemy_pieces_pos:
					break				

		# right botom - left top diagonal
		for i in range(8):
			if util.isNotOutofBounds(x-i, y+i):
				# restricting movement because of other player pieces
				if (x-i,y+i) in self.player_pieces_pos:
					break
				valid_moves.append((x-i,y+i))
				# restricting movement because of enemy pieces
				if (x-i,y+i) in self.enemy_pieces_pos:
					break

		for i in range(8):
			if util.isNotOutofBounds(x+i, y-i):
				# restricting movement because of other player pieces
				if (x+i,y-i) in self.player_pieces_pos:
					break
				valid_moves.append((x+i, y-i))
				# restricting movement because of enemy pieces
				if (x+i,y-i) in self.enemy_pieces_pos:
					break

		# for (x,y) in valid_moves:
		# 	# Check for collisions
		# 	action = Action(self, (x,y), self.player_pieces, self.enemy_pieces)
		# 	if not action.isValid(): valid_moves.remove((x,y))

		return valid_moves

class King(Piece):

	def __init__(self, color, (x,y), index):
		Piece.__init__(self, color, (x,y), index)
		self.points = 1000

	def toString(self):
		return "K"

	def validMoves(self, config):
		valid_moves = []
		x,y = self.pos
		
		final_pos = [(x+1,y),(x,y+1),(x+1,y+1),(x-1,y),(x,y-1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]

		for posx,posy in final_pos:
			if util.isNotOutofBounds(posx, posy):
				action = Action(self, (posx, posy), config)
				if action.isValid():
					valid_moves.append((posx,posy))

		# Castling ?

		return valid_moves