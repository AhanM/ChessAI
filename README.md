# ChessAI
### The Classic Chess Game with AI Features

##### For PvP execute:
$ python chess-pvp.py

##### For P v Computer execute:
$ python chess-pvc.py
	
#### Nomenclature:
  - P => Pawn
  - N => Knight
  - B => Bishop
  - R => Rook
  - Q => Queen
  - K => King
  
#### Move Syntax:
Piece Character - Initial Coordinate - New Coordinate

Example: White's Turn: P - (4,1) - (4,2)

#### To do:
 - Implement Castling
 - Test all features

#### Problems:
 - Extremely Slow AI Agents due to sub-optimal implementation
 - Typing out moves is a noisome task
 - Coordinates for black are confusing
 - User Experience is lacklustre without a GUI
 - Command Line argument support absent
 - Unable to diffrentiate between black and white pieces on terminal board

#### Solutions:
 - Using a bit board for heavy computations
 - Creating a coordinate converter for black