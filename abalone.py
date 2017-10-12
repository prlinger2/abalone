from __future__ import division
from __future__ import print_function
import collections
import math

# Notes:
# use a dictionary to map each Hex using the coords as the key.
# Lists are ordered (accessed via position), dictionaries are not (keys).
# use a tuple as the key (q,r,s)
# Don't use offset coords.  Use them for rectangles.
# (q,r,s) == (x,y,z)


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
	def __init__(self, r):
		center_hex = Hex(0, 0, 0)
		tiles = {center_hex.key : center_hex};
		#range(start, stop(upto,not incl), step):
		for dq in range(-r, r+1, 1):
			for dr in range(max(-r, -dq-r), min(r, -dq+r) + 1, 1):
				ds = -dq-dr #this calculates the third coord by dx+dy+dz=0
				tiles[(dq, dr, ds)] = Hex(dq, dr, ds)
		self.tiles = tiles
		self.radius = r

	def init_board_state(self):
		directions = [(1,-1,0), (1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1), (0,-1,1)]
		
		black = [(0, 0, 0), (1, -1, 0), (2, -2, 0)]
		white = [(-1, 1, 0), (-2, 2, 0)]
		
		for b in black:
			self.tiles[b].add_marble("black")
		for w in white:
			self.tiles[w].add_marble("white")

		
	
	# tests if marbles are in a valid line.  Tests inline and adjacency.
	# requires: 2 or more hexes that contain marbles.
	# returns the line that the marbles lie on or False**?(False or what?)
	def valid_line(self, marbles):
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
	
	# translate_marbles() pushing_list and pushed_list one hex in direction
	# Eg. pushing_list is 3 black pushing 2 white (pushed_list)
	# Note: the hex past the end of pushed list (the one that will be occupied after
	# the push) is empty. (and it must be)
	# Note: both lists are sorted in the same direction
	# the tip is the last element in pushing_list
	# Requires: 2 or more marbles/hexes in total
	def translate_marbles(self, direction, index, pushing_list, pushed_list):
		pushing_len = len(pushing_list)
		pushed_len = len(pushed_list)
		
		#furthest marble being pushed moved
		temp_hex = pushed_list[pushed_len - 1]
		temp_key = (temp_hex.q + direction[0], temp_hex.r + direction[1], 
					temp_hex.s + direction[2])
		self.tiles[temp_key].marble = temp_hex.marble
		
		# moves the pushing list. It is arbitrary if tip or tail moves first since len>=2	
		temp_hex = pushing_list[0] #this is the tail
		temp_key = (temp_hex.q + direction[0], temp_hex.r + direction[1], 
					temp_hex.s + direction[2])
		self.tiles[temp_key].marble = temp_hex.marble
		
		temp_hex = pushing_list[pushing_len - 1]
		temp_key = (temp_hex.q + direction[0], temp_hex.r + direction[1], 
					temp_hex.s + direction[2])
		self.tiles[temp_key].marble = temp_hex.marble
		
		#makes sure last marble to move is deleted
		if(index == 0): #leading with tail.
			self.tiles[pushing_list[pushing_len - 1].key].del_marble()
		else: #leading with tip	
			self.tiles[pushing_list[0].key].del_marble()
			
		
		
		
	# move_inline() moves marbles that are oriented in a line.
	# index is either 0 for leading with tail or [length - 1] for leading with tip
	### ADD FOR WHEN NOT PUSHING ANYTHING
	# the problem is that the loop is based on length (of sorted), not how many beuing pushed
	def move_inline(self, direction, index, length, sorted_marbles):
		pushed_list = []
		for i in range(1, length + 1, 1):
			cur_coord = ( #coord of next hex, direction vector, i for each subsequent, sorted marbles for the translation from the origin to the tip
				direction[0] * i + sorted_marbles[index].key[0],
				direction[1] * i + sorted_marbles[index].key[1],
				direction[2] * i + sorted_marbles[index].key[2]
				)
			
			#print(pushed_list)
			print(self.tiles[cur_coord].is_empty())
			if not(cur_coord in self.tiles): #tests if pushing to a hex.  If not, the marble will be eliminated
				# don't need to delete, the marble is just overwritten in translate_marbles
				self.translate_marbles(direction, index, sorted_marbles, pushed_list)
			elif self.tiles[cur_coord].is_empty(): #pushing to empty hex. Now just move
				# remember case where say 3 push 2, hits empty and has to rewrite
				self.translate_marbles(direction, index, sorted_marbles, pushed_list)
				return True
			elif i >= length: #when there is an equal force.  Cannot push.
				return False
			elif sorted_marbles[0].marble == self.tiles[cur_coord].marble:
				#when trying to push a separated marble of same colour. Eg. BBBWB->
				return False
			
			pushed_list += [self.tiles[cur_coord]]
	
	# move_adjacent() moves a line of marbles in direction.  This is for sideways (no pushing)
	# length is the length of sorted_marbles
	def move_adjacent(self, direction, length, sorted_marbles):
		for i in range(0, length):
			temp_hex = sorted_marbles[i]
			temp_key = (temp_hex.key[0] + direction[0], 
						temp_hex.key[1] + direction[1], 
						temp_hex.key[2] + direction[2])
			self.tiles[temp_key].marble = sorted_marbles[i].marble
			sorted_marbles[i].del_marble
	
	
	# moves the marbles on the hexes
	# Requires: 1 or more Hexes that containing marbles
	def move(self, direction, *coords):
		
		length = len(coords)
		# converts coords entered into references to tiles
		marbles = [None] * length
		for i in range(0, length, 1):
			marbles[i] = self.tiles[coords[i]]
			
		#makes sure one is trying to push without a marble
		for ahex in marbles:
			assert(ahex.marble != "empty"), "Pushing with empty hex. move() in HexBoard"
		
		
		
		if length == 1:
			pass #actions for when only 1 marble
		assert(self.valid_line(marbles)), "Not a valid selection of marbles; move() in HexBoard"
		marble_line = HexLine(marbles[0], marbles[1]) #note that these marbles are inline
		dir_line = HexLine(Hex(direction[0], direction[1], direction[2]), Hex(0, 0, 0))
		
		# The tip is the highest or rightmost hex in a line of marbles (if on xy plane)
		# Finding the tip uses the property that in a line, one coord will not change
		#if q, find greatest r
		#if r find smallest s
		#if s find greatest q
		sorted_marbles = [None] * length # the tip is the last element in sorted_marbles
		if marble_line.axis == 'q':
			sorted_marbles = sorted(marbles, key=lambda x: x.r, reverse=False)
		elif marble_line.axis == 'r':
			sorted_marbles = sorted(marbles, key=lambda x: x.s, reverse=True)
		else: #axis is s
			sorted_marbles = sorted(marbles, key=lambda x: x.q, reverse=False)
						
		if dir_line.axis == marble_line.axis: #if true, the mvmt is forwards
			#loop of the next length hexes in direction to see if occupied.			
			if (direction == (1,-1,0)) or (direction == (1,0,-1)) or (direction == (0,1,-1)): #leading with tip
				self.move_inline(direction, length - 1, length, sorted_marbles)					
			else: # leading with tail. Only diff is using sorted_marbles[0] since tail
				self.move_inline(direction, 0, length, sorted_marbles)
					
		else: #the movement is adjacent
			for i in range(0, length):
				temp_hex = sorted_marbles[i]
				temp_key = (temp_hex.key[0] + direction[0], 
							temp_hex.key[1] + direction[1], 
							temp_hex.key[2] + direction[2])
				if not(temp_key in self.tiles):
					return False
				if not(self.tiles.is_empty()):
					return False
			self.move_adjacent(direction, length, sorted_marbles)		


# generates a HexBoard of radius r centered around (q,r,s)=(0,0,0)
# This works by satisfing the property of cube coords dx+dy+dz=0
###### OBSOLETE.  USE HexBoard constructor
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


def test_hexboard():
	directions = [(1,-1,0), (1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1), (0,-1,1)]
	b = HexBoard(4)
	# init works
	b.init_board_state()
	black = [(0, 0, 0), (1, -1, 0), (2, -2, 0)]
	white = [(-1, 1, 0), (-2, 2, 0)]
	#print(b.tiles[(0, 0, 0)].marble)
	
	print("(-3, 3, 0)w: " + b.tiles[(-3, 3, 0)].marble)
	print("(-2, 2, 0)w: " + b.tiles[(-2, 2, 0)].marble)
	print("(-1, 1, 0)b: " + b.tiles[(-1, 1, 0)].marble)
	print("(0, 0, 0)b: " + b.tiles[(0,0,0)].marble)
	print("(1, -1, 0)b: " + b.tiles[(1, -1, 0)].marble)
	print("(2, -2, 0)e: " + b.tiles[(2, -2, 0)].marble)
	
	b.move(directions[3], black[0], black[1], black[2])	
	print("(-3, 3, 0)w: " + b.tiles[(-3, 3, 0)].marble)
	print("(-2, 2, 0)w: " + b.tiles[(-2, 2, 0)].marble)
	print("(-1, 1, 0)b: " + b.tiles[(-1, 1, 0)].marble)
	print("(0, 0, 0)b: " + b.tiles[(0,0,0)].marble)
	print("(1, -1, 0)b: " + b.tiles[(1, -1, 0)].marble)
	print("(2, -2, 0)e: " + b.tiles[(2, -2, 0)].marble)
	
test_hexboard()


