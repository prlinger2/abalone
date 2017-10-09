from __future__ import division
from __future__ import print_function
import collections
import math

# Notes:
# use a dictionary to map each Hex using the coords as the key.
# Lists are ordered (accessed via position), dictionaries are not (keys).
# use a tuple as the key (q,r,s)
# Don't use offset coords.  Use them for rectangles.


#base class for creating a single hex.
# q,r,s are coordinates.
class Hex:	
	def __init__(self, q, r, s):
		self.q = q
		self.r = r
		self.s = s
		self.key = (q, r, s);
		self.marble = "empty" #hexes are initialized without marbles.
	
	# add_marble(colour) adds a marble to hex of colour.  
	# This can also override and replace marbles.
	def add_marble(self, colour):
		self.marble = colour
	
	# del_marble() deletes the marble on the hex.
	def del_marble(self):
		self.marble = "empty"
	
	#returns true if the hex is empty
	def is_empty(self):
		return (self.marble == "empty")

# represents a line on a HexBoard.
# Lines denoted by: axis + trans.  Where axis is one of 3 axis (possible orientations)
#	and trans is how far the line is transformed from passing through the origin
# requires: two hexes that are inline on an integer linear combination of the axis in R^3.
####### NOT IN USE
class HexLine:
	#line_directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1)]
	def __init__(self, hex1, hex2):
		# find the unchanging coord, that is the axis
		if hex1.q == hex2.q:
			self.axis = 'q' #line_directions[0]
			self.trans = hex1.q
		elif hex1.r == hex2.r:
			self.axis = 'r' #line_directions[1]
			self.trans = hex1.r
		else:
			self.axis = 's' #line_directions[2]
			self.trans = hex1.s		
		

class HexBoard:
	#the tiles is the dict of all hexes.
	def __init__(self, tiles, radius):
		self.tiles = tiles
		self.radius = radius

	def init_board_state():
		pass
	
	# tests if marbles are in a valid line.  Tests inline and adjacency.
	# requires: 2 or more hexes that contain marbles.
	# returns the line that the marbles lie on or False**?(False or what?)
	def valid_line(self, *marbles):
		assert(len(marbles) < 4),"Trying to move 4+ marbles. valid_line() in class HexBoard"
		length = len(marbles)
		line_axis = None
		if marbles[0].q == marbles[1].q:
			line_axis = 'q'
		elif marbles[0].r == marbles[1].r:
			line_axis = 'r'
		else:
			line_axis = 's'
			
		adj_axis = 'q'
		if line_axis == adj_axis:
			adj_axis = 'r'				
		adj_axis_values = [None] * length
		line_axis_values = [None] * length
		for i in range(0, length, 1): # I believe length since upto no incl
			adj_axis_values[i] = getattr(marbles[i], adj_axis) #get the value of the coord that should be changing.  Like marbles[i].q/r/s
			line_axis_values[i] = getattr(marbles[i], line_axis)
		adj_axis_values = sorted(adj_axis_values) #sort in ascending order to test adjacency
		for i in range(1, length, 1): #makes sure there is a diff of 1. Otherwise not adj
			if (((adj_axis_values[i] - adj_axis_values[i - 1]) != 1) or 
				((line_axis_values[i] - line_axis_values[i - 1]) != 0)):
				return False
		return True				
	
	# moves the marbles on the hexes
	# Requires: 1 or more Hexes that containing marbles
	def move(direction, *marbles):
		if len(marbles) == 1:
			pass #actions for when only 1 marble
			
		

# generates a HexBoard of radius r centered around (q,r,s)=(0,0,0)
# This works by satisfing the property of cube coords dx+dy+dz=0
def generate_hex_board(r):
	center_hex = Hex(0, 0, 0)
	tiles = {center_hex.key : center_hex};
	
	#range(start, stop(upto,not incl), step):
	for dq in range(-r, r+1, 1):
		for dr in range(max(-r, -dq-r), min(r, -dq+r) + 1, 1):
			ds = -dq-dr #this calculates the third coord by dx+dy+dz=0
			tiles[(dq, dr, ds)] = Hex(dq, dr, ds)
	
	return HexBoard(tiles, r)


########################################################
# Tests:
def test_generate_hex_board():
	board = generate_hex_board(4)
	for x in board.tiles:
		print(x)

#test_generate_hex_board()
def test_valid_line():
	a = Hex(3, 0, -3)
	b = Hex(3, -1, -2)
	c = Hex(3, -2, -1)
	d = Hex(3, -3, 0)
	e = Hex(0, 0, 0)
	board = HexBoard(a, 1)
	if(not board.valid_line(a, b)):
		print("test_valid_line failed")


#test_valid_line()




