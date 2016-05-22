
from pieces import *
from action import Action
import sys

class Config(object):
	"""
	A simple structure responsible for allowing
	access to useful state features such as:

	- Player Pieces
	- Player Piece Positions
	- Enemy Pieces
	- Enemy Piece Positions
	"""
	def __init__(self, whitePieces, blackPieces):
		super(Config, self).__init__()
		self.whitePieces = whitePieces
		self.blackPieces = blackPieces

	def update(self, whitePieces, blackPieces):
		self.whitePieces = whitePieces
		self.blackPieces = blackPieces

	def getPlayerPieces(self, color):

		if color == "White":
			return self.whitePieces
		else:
			return self.blackPieces

	def getPlayerPositions(self, color):

		pieces = self.getPlayerPieces(color)
		return [piece.pos for piece in pieces]

	def getEnemyPieces(self, color):

		if color == "White":
			return self.blackPieces
		else:
			return self.whitePieces

	def getEnemyPositions(self, color):

		pieces = self.getEnemyPieces(color)
		return [piece.pos for piece in pieces]
		

class State(object):
	"""
	A State object will encode information about the pieces and their respective positions
	on the board. A State object will also have the ability to generate successors, to test
	for checks and checkmates as well as control the movements of pieces and turns of players.
	"""
	def __init__(self):
		super(State, self).__init__()
		self.capturedPieces = []
		
		# Initialize pieces
		k = King("White", (4,0), 0)
		q = Queen("White", (3,0), 1)
		n1 = Knight("White", (1,0), 2)
		n2 = Knight("White", (6,0), 3)
		b1 = Bishop("White", (2,0), 4)
		b2 = Bishop("White", (5,0), 5)
		r1 = Rook("White", (0,0), 6)
		r2 = Rook("White", (7,0), 7)

		_k = King("Black",(4,7), 0)
		_q = Queen("Black", (3,7), 1)
		_n1 = Knight("Black", (1,7), 2)
		_n2 = Knight("Black", (6,7), 3)
		_b1 = Bishop("Black", (2,7), 4)
		_b2 = Bishop("Black", (5,7), 5)
		_r1 = Rook("Black", (0,7), 6)
		_r2 = Rook("Black", (7,7), 7)

		whitePieces = [k,q,n1,n2,b1,b2,r1,r2]
		blackPieces = [_k,_q,_n1,_n2,_b1,_b2,_r1,_r2]

		for i in range(8):
			p = Pawn("White", (i,1), 8+i)
			whitePieces.append(p)

		for i in range(8):
			p = Pawn("Black", (i,6), 8+i)
			blackPieces.append(p)

		self.pieces = whitePieces + blackPieces

		# Create Config object
		self.config = Config(whitePieces, blackPieces)

		self.board = [["-" for x in range(8)] for x in range(8)] 
		self.initBoard() 

	def initBoard(self):
		# configuring board positions
		board = self.board
		
		for piece in self.pieces:
			board[piece.x][piece.y] = piece

		self.board = board

	def reinitBoard(self):
		self.board = [["-" for x in range(8)] for x in range(8)] 
		self.initBoard()

	# Displays white's pieces nearer
	def whiteDisplay(self):
		size = 8
		for i in range(size-1, -1,-1):
			for j in range(size):
				if isinstance(self.board[j][i], Piece):
					print self.board[j][i].toString(),
				else:
					print self.board[j][i],
				
			print ""

	# Displays black's pieces nearer
	def blackDisplay(self):
		size = 8
		for i in range(size):
			for j in range(size):
				if isinstance(self.board[j][i], Piece):
					print self.board[j][i].toString(),
				else:
					print self.board[j][i],
				
			print ""

	def getSuccessor(self, action):
		successorState = State()
		
		successorState.capturedPieces = self.capturedPieces
		successorState.config.whitePieces = list(self.config.whitePieces)
		successorState.config.blackPieces = list(self.config.blackPieces)

		if action.isCapture():
			capturedPiece = action.capturedPiece()
			successorState.capturedPieces.append(capturedPiece)

			successorState.board[capturedPiece.pos[0]][capturedPiece.pos[1]] = "-"

			if capturedPiece.color == "White":
				successorState.config.whitePieces.remove(capturedPiece)
			else:
				successorState.config.blackPieces.remove(capturedPiece)

		piece = action.piece

		char = piece.toString()

		if char == "P":
			newPiece = Pawn(piece.color, action.newPos, piece.index)
		elif char == "N":
			newPiece = Knight(piece.color, action.newPos, piece.index)
		elif char == 'B':
			newPiece = Bishop(piece.color, action.newPos, piece.index)
		elif char == 'R':
			newPiece = Rook(piece.color, action.newPos, piece.index)
		elif char == 'Q':
			newPiece = Queen(piece.color, action.newPos, piece.index)
		else:
			newPiece = King(piece.color, action.newPos, piece.index)

		if piece.color == "White":

			if piece in successorState.config.whitePieces:
				successorState.config.whitePieces.remove(piece)
			successorState.config.whitePieces.append(newPiece)
		else:
			if piece in successorState.config.blackPieces:
				successorState.config.blackPieces.remove(piece)
			successorState.config.blackPieces.append(newPiece)

		successorState.pieces = successorState.config.whitePieces + successorState.config.blackPieces

		# Change Board
		successorState.reinitBoard()
		newx, newy = action.newPos
		oldx, oldy = action.piece.pos
		successorState.board[newx][newy] = newPiece
		successorState.board[oldx][oldy] = "-"

		return successorState

	def generateActionFromString(self, moveString):
		# moveString should look like: P - (1,2) - (1,3)
		# generate action from moveString

		pieceChar = moveString[0]
		curPos = int(moveString[4:9][1]), int(moveString[4:9][3])
		newPos = int(moveString[12:][1]), int(moveString[12:][3])

		# Identify the piece
		for p in self.pieces:
			if p.pos == curPos:
				piece = p

		if piece.toString() != pieceChar:
			print "Error: Invalid Action"
			sys.exit()

		action = Action(piece, newPos, self.config)

		return action

	def getScore(self, player):
		enemyScore = 0
		playerScore = 0
		for piece in self.capturedPieces:
			if piece.color == player.color:
				enemyScore += piece.points
			else: playerScore += piece.points

		return enemyScore, playerScore


	def gameOver(self, white, black):

		if white.checkMate(self):
			print "Checkmate. Black Wins!!!!"
			return True
		elif black.checkMate(self):
			print "Checkmate. White Wins!!!"
			return True

		return False

