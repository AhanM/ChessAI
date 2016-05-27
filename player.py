# player.py
# ---------

from action import *

class Player(object):
	'''
	Player class is responsible for maintaining
	black and white neutrality and for defining properties 
	of players such as:

	- Making a move
	- Keeping track of pieces
	- Checks
	'''
	def __init__(self, color, pieces, enemyPieces):
		super(Player, self).__init__()
		self.color = color
		self.check = False

		self.pieces = pieces
		for piece in pieces:
			if piece.toString() == "K":
				self.king = piece
		# self.enemyPieces = enemyPieces

		if color == "White": 
			self.turn = True
		else: 
			self.turn = False

	def getLegalActions(self, state):
		'''
		Generate a list of all valid moves for the player
		'''
		moves = []

		for piece in self.pieces:
			if len(piece.validMoves(state.config)) > 0:
				for newPos in piece.validMoves(state.config):
					
					action = Action(piece, newPos, state.config)
					moves.append(action)

		# Remove moves which lead to a check
		for action in moves:
			nextState = state.getSuccessor(action)
			if self.kingUnderAttack(nextState):
				moves.remove(action)
				state.pinnedPieces += 1

		return moves

	def kingUnderAttack(self, state):
		enemyPieces = state.config.getEnemyPieces(self.color)
		for p in enemyPieces:
			if self.king.pos in p.validMoves(state.config):
				self.check = True
				return True
		return False
		

	def makeMove(self, state, action):
		'''
		Check if the move is a valid one and then
		change the state and piece positions accordingly
		'''
		if action.toString() in [act.toString() for act in self.getLegalActions(state)]:
			nextState = state.getSuccessor(action)
			self.pieces = nextState.config.getPlayerPieces(self.color)
			self.enemyPieces = nextState.config.getEnemyPieces(self.color)
			return nextState

		else:
			print "Error: Invalid action passed to Player.makeMove(..)"
			return None

	def checkMate(self, state):
		'''
		Return True if there are no possible moves for Player
		otherwise return False
		'''
		return self.getLegalActions(state) == []