# agent.py
# --------
import util

def scoreEvaluationFn(gameState, player):
	'''
	This default evaluation function just returns the score of the state.
	'''
	enemyScore, playerScore =  gameState.getScore(player)

	return playerScore - enemyScore

def betterEvaluationFn(gameState, player):
	'''
	Insane piece killing evaluation function

	DESCRIPTION: 
	< Considering: Mobility, Number of Doubled, Isolated Pawns and Pinned Pieces, 
	King checked, Queen Trapped >

	Pawn Structure:
	  - Penalise doubled, backward and blocked pawns.
	  - Encourage pawn advancement where adequately defended.
	  - Encourage control of the centre of the board.
	Piece Placement:
	  - Encourage knights to occupy the centre of the board.
	  - Encourage bishops to occupy principal diagonals.
	  - Encourage queens and rooks to defend each other and attack.
	  - Encourage 7th rank attacks for rooks.
	Passed Pawns:
	  - These deserve a special treatment as they are so important.
	  - Check for safety from opposing king and enemy pieces.
	  - Test pawn structure for weaknesses, such as hidden passed pawns.
	  - Add enormous incentives for passed pawns near promotion.
	King Safety
	  - Encourage the king to stay to the corner in the middlegame.
	  - Try to retain an effective pawn shield.
	  - Try to stop enemy pieces from getting near to the king.

	'''
	mobility = len(player.getLegalActions(gameState))
	enemyScore, playerScore = gameState.getScore(player)
	pawns = [piece for piece in player.pieces if piece.toString() == "P"]
	actions = player.getLegalActions(gameState)

	NumOfDoubledPawns = 0

	for pawn in pawns:
		if player.color == "White":
			if (pawn.pos[0], pawn.pos[1]+1) in [pawn.pos for pawn in pawns]:
				NumOfDoubledPawns += 1
		else:
			if (pawn.pos[0], pawn.pos[1]-1) in [pawn.pos for pawn in pawns]:
				NumOfDoubledPawns += 1


	NumOfIsolatedPawns = 0

	for pawn in pawns:
		if util.computeMinDistFromOtherPieces(pawn, player.pieces) > 4:
			NumOfIsolatedPawns += 1

	NumOfPinnedPieces = gameState.pinnedPieces

	centralControl = 0 # checking control over the coordinates:  (2,3) (3,3) (4,3) (5,3) (2,4) (3,4) (4,4) (5,4)
	central_coords = [(2,3),(3,3),(4,3),(5,3),(2,4),(3,4),(4,4),(5,4)]

	pieces_pos = [piece.pos for piece in player.pieces]
	actions_pos = [action.newPos for action in actions]

	for coord in central_coords:
		if coord in pieces_pos or coord in actions_pos:
			centralControl += 1

	sum = 10 * mobility - 20 * NumOfPinnedPieces - 5* (NumOfIsolatedPawns+NumOfDoubledPawns) + 100 * (playerScore-enemyScore) + 50 * centralControl
	
	return sum

class Agent(object):
	"""An abstract class for AlphaBeta and Expectimax agents"""
	def __init__(self, player, enemy, evalFn=scoreEvaluationFn, depth="2"):
		super(Agent, self).__init__()
		self.player = player
		self.color = player.color
		self.enemy = enemy
		self.evaluationFunction = evalFn
		self.depth = int(depth)
		

	def getAction(self, args):

		util.raiseNotDefined()


class AlphaBetAgent(Agent):
	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		value, index = self.max_value(gameState, self.depth, float('-inf'), float('inf'))

		return self.player.getLegalActions(gameState)[index]


	def max_value(self, gameState, curDepth, alpha, beta):
		v = float('-inf')
		# print "Max node"
		# print "Current Depth:", curDepth

		legalActions = self.player.getLegalActions(gameState)
		counter = 0

		# Check if this is an end state and whether the depth has been reached
		if len(legalActions) == 0 or curDepth == 0:
			# print "Returns: ", self.evaluationFunction(gameState, self.player)
			return self.evaluationFunction(gameState, self.player), None

		for i, action in enumerate(legalActions): 
			successor = gameState.getSuccessor(action)

			# Recurse if depth has not been reached
			newv = max(v, self.min_value(successor, curDepth, alpha, beta))

			# keep track of the index of the best action
			if newv != v: counter = i

			v = newv

			if v > beta: return v, counter # pruning

			alpha = max(alpha, v)

		return v, counter

	def min_value(self, gameState, curDepth, alpha, beta):
		v = float('inf')

		# print "Min Node"
		# print "Current Depth:", curDepth

		legalActions = self.player.getLegalActions(gameState)

		# Check if this is an end state
		if len(legalActions) == 0:
			# print "Returns: ", self.evaluationFunction(gameState, self.enemy)
			return self.evaluationFunction(gameState, self.enemy)

		for action in legalActions:
			successor = gameState.getSuccessor(action)

			# Switch to MAX agent
			v = min(v, self.max_value(successor, curDepth-1, alpha, beta)[0])

			if v < alpha: return v # pruning
			beta = min(beta, v)

		return v


class ExpectimaxAgent(Agent):
	"""
	A simple Expectimax Agent
	"""

	def getAction(self, gameState):

		value, index = self.max_value(gameState, self.depth)

		return self.player.getLegalActions(gameState)[index]

	def max_value(self, gameState, curDepth):

		legalActions = self.player.getLegalActions(gameState)
		counter = 0
		v = float('-inf')

		if len(legalActions) == 0 or curDepth == 0:
			return self.evaluationFunction(gameState, self.player), None
	
		for i, action in enumerate(legalActions):
			successor = gameState.getSuccessor(action)

			newv = max(v, self.expect_value(successor, curDepth))

			# keep track of the index of the best action
			if newv != v: counter = i

		v = newv

		return v, counter

	def expect_value(self, gameState, curDepth):

		legalActions = self.player.getLegalActions(gameState)
		total = 0

		if len(legalActions) == 0:
			return self.evaluationFunction(gameState, self.enemy)

		for action in legalActions:
			successor = gameState.getSuccessor(action)

			# Switch to MAX agent
			total = total + self.max_value(successor, curDepth-1)[0]

		return ( float(total) / len(legalActions) )
		