d = {(2, -1, -1):"a", (1, -2, 1):"b"}

class Hex:	
	def __init__(self, q, r, s):
		self.q = q
		self.r = r
		self.s = s
		self.key = (q, r, s);
		self.marble = "empty" #hexes are initialized without marbles.


def test(tst, *args):
	li = [None]
	for arg in args:
		li += [arg]
		#print(arg)
	print(li)
	print(len(li))
	

a = Hex(3, -1, -2)
b = Hex(2, -1, -1)
c = Hex(1, -1, 0)


test(1, a,b,c)