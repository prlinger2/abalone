# abalone
A recreation of the game played with marbles on a hexagonal board.

Rules:
1. A player may move up to 3 marbles one space in any direction.
2. One may push opponents marbles if:
	i. The opposing force is smaller than the pushing force.
	ii. The number of moving marbles for each colour does not exceed 2 (this removes the case where a player tries to push one of their marbles separated by an opponents marble).
3. The game is won by the first player to eject 6 of the opponents marbles.


Definitions:
	1. (q,r,s) == (x,y,z)
	2. The angles are defined the same was as a unit circle.  Counterclockwise, 360 degrees.


Notes/Brainstorming:
Movement:
	- test if 1 marble being moved.
		- if yes: test if hex in direction is empty, if yes; move
	- test if less than 4 marbles being moved
	- test if all marbles are in a line.
		- this should also test that they are all in a line with no breaks.
	- test to see if moving sideways or forwards (inline or not)
		- if inline:
			- test if the adjacent in a line is occupied.
				- if yes:
					See how deep the line goes (until it hits an empty space.
					If it hits one of the same colour, short circuit to invalid move.
				- if no: add marble of same colour to front. delete
		- if moving sideways:
			- test if all hexes adjacent in direction are empty
			- add all the marbles and delete all the original ones.

Lines on a HexBoard:
- A line can be defined by two coords out of (x,y,z) that move and the third one that doesn't change denotes the min distance from the origin the line passes through.


More Notes:
	- For efficieny, I should perhaps find the endpoints of the line of marbles in move().  Then rewrite valid_line.
	
	