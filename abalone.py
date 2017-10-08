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


class HexBoard:
	#the tiles is the dict of all hexes.
	def __init__(self, tiles, radius):
		self.tiles = tiles
		self.radius = radius


class Hex:	
	def __init__(self, q, r, s):
		self.q = q
		self.r = r
		self.s = s
		self.key = (q, r, s);

#adds two hexes together.
def hex_add(a, b):
	return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

#subtracts hex b from hex a
def hex_subtract(a, b):
	return Hex(a.q - b.q, a.r - b.r, a.s - b.s)

#scales hex a by k.
def hex_scale(a, k):
	return Hex(a.q * k, a.r * k, a.s * k)

hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]

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
	board = generate_hex_board(1)
	for x in board.tiles:
		print(x)
# test_generate_hex_board()



