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

	DESCRIPTION: <  >
	'''

	util.raiseNotDefined()

class Agent(object):
	"""An abstract class for AlphaBeta and Expectimax agents"""
	def __init__(self, player, evalFn=scoreEvaluationFn, depth="2"):
		super(Agent, self).__init__()
		self.player = player
		self.color = color
		self.evaluationFunction = None
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

			legalActions = self.player.getLegalActions(gameState)
			counter = 0

			# Check if this is an end state and whether the depth has been reached
			
			if len(legalActions) == 0 or curDepth == 0:
				return self.evaluationFunction(gameState), None

			for i, action in enumerate(legalActions): 
				successor = gameState.generateSuccessor(0, action)

			# Recurse if depth has not been reached
			newv = max(v, self.min_value(successor, curDepth, alpha, beta))

			# keep track of the index of the best action
			if newv != v: counter = i

			v = newv

			if v > beta: return v, counter # pruning
			alpha = max(alpha, v)

			return v, counter

		def min_value(self, gameState, curDepth, alpha, beta):
			v = float(inf)

			legalActions = self.player.getLegalActions(gameState)

			# Check if this is an end state
			if len(legalActions) == 0:
				return self.evaluationFunction(gameState)

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

	def max_val(self, gameState, curDepth):

		legalActions = self.getLegalActions(gameState)
		counter = 0
		v = float('-inf')

		if len(legalActions) == 0 or curDepth == 0:
			return self.evaluationFunction(gameState), None
	
		for i, action in enumerate(legalActions):
			successor = gameState.getSuccessor(action)

		newv = max(v, self.expect_value(successor, curDepth))

		# keep track of the index of the best action
		if newv != v: counter = i

		v = newv

	  return v, counter

	def expect_val(self, gameState, curDepth):

		legalActions = self.getLegalActions(gameState)
		total = 0

		if len(legalActions) == 0:
			return self.evaluationFunction(gameState)

		for action in legalActions:
			successor = gameState.getSuccessor(action)

			# Switch to MAX agent
			total = total + self.max_value(successor, curDepth-1)[0]

		return ( float(total) / len(legalActions) )
		