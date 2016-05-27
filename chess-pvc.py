from game import State
from player import *
from agent import AlphaBetAgent, betterEvaluationFn
import time

def main():

	print "Welcome to Chess v 2.0"

	state = State()

	white = Player("White", state.config.whitePieces, state.config.blackPieces)
	black = Player("Black", state.config.blackPieces, state.config.whitePieces)
	agent = AlphaBetAgent(black, white, depth="2", evalFn=betterEvaluationFn)

	while not state.gameOver(white, black):

		if white.turn:
			white.turn = False
			black.turn = True

			state.whiteDisplay()

			print "Possible moves:"
			actions = white.getLegalActions(state)
			for action in actions:
				print action.piece.pos, action.toString()

			moveString = raw_input("White's Turn: ")
			player = white

			moveString.strip()
			
			if moveString == "q":
				break

			action = state.generateActionFromString(moveString)

			nextState = white.makeMove(state, action)

			black.pieces = white.enemyPieces

		elif black.turn:
			black.turn = False
			white.turn = True

			state.blackDisplay()

			actions = black.getLegalActions(state)
			for act in actions:
				print act.piece.pos, act.toString()

			t1 = time.time()

			action = agent.getAction(state)

			t2 = time.time()

			nextState = black.makeMove(state, action)

			white.pieces = black.enemyPieces

			print "Black's Turn:", action.piece.pos, action.toString()
			print "Execution time: ", t2-t1, "secs"



		

		print "--------------------------------------"
		print ""

		del state
		state = nextState

	print "Game Over"

if __name__ == '__main__':
	main()