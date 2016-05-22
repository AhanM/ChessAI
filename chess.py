
from game import State
from player import *

def main():

	print "Welcome to Chess v 2.0"

	state = State()

	white = Player("White", state.config.whitePieces, state.config.blackPieces)
	black = Player("Black", state.config.blackPieces, state.config.whitePieces)

	while not state.gameOver(white, black):

		if white.turn:
			state.whiteDisplay()

			white.turn = False
			black.turn = True

			print "Possible moves:"
			actions = white.getLegalActions(state)
			for action in actions:
				print action.piece.pos, action.toString()

			moveString = raw_input("White's Turn: ")
			player = white

		elif black.turn:
			state.blackDisplay()

			black.turn = False
			white.turn = True

			print "Possible moves:"
			actions = black.getLegalActions(state)
			for action in actions:
				print action.piece.pos, action.toString()

			moveString = raw_input("Black's Turn: ")
			player = black


		moveString.strip()
		if moveString == "q":
			break

		action = state.generateActionFromString(moveString)
		
		nextState = player.makeMove(state, action)

		print "--------------------------------------"
		print ""

		del state
		state = nextState

	print "Game Over"

if __name__ == '__main__':
	main()