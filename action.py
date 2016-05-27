# action.py
# ---------

from game import *

class Action(object):
	'''
	An Action object would basically be used to formalize moves 
	defined by a paticular piece and it's new position.

	It will be used to determine whether an action is feasable in terms of 
	collisions etc. or not and whether an action involves a capture.
	'''
	def __init__(self, piece, (x,y), config):
		self.piece = piece
		self.newPos = (x,y)

		self.color = piece.color

		self.promotion = False # For Pawn Promotion

		self.player_pieces = config.getPlayerPieces(self.color)
		self.enemy_pieces = config.getEnemyPieces(self.color)

	def toString(self):
		return self.piece.toString() + " -> " + str(self.newPos)

	def isValid(self):
		''' Checks for direct position collisions with same colored pieces'''
		for piece in self.player_pieces:
			if self.newPos == piece.pos:
				return False
		return True

	def isCapture(self):
		'''
		Returns whether this action results in a capture or not
		'''
		return self.newPos in [enemypiece.pos for enemypiece in self.enemy_pieces]

	def capturedPiece(self):
		'''
		Returns the piece object which was captured in the 
		respective action
		'''
		for enemypiece in self.enemy_pieces:
			if self.newPos == enemypiece.pos:
				return enemypiece
		return None