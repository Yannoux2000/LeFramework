from .Objs import *
from .ConstVec import *

class Node(Target):
	def __init__(self, vec = [0,0,0]):
		super(Node,self).__init__(Vec3(vec))

		self.i = 0			#it's reference
		self.parent = None	#reference towards best previous node, None if start
		self.cost = 0		#cost related to the distance from the start achieved

	def calcCost(self, other):
		return other.cost + other.distance(self)# - 250 #bias to get a little more steps than needed

	def setCost(self, other):
		self.cost = self.calcCost(other)

	def asTarget(self):
		return Target(self.loc)

	def __str__(self):
		return str(self.loc)

class Path():
	def __init__(self, path, reloop = True):
		self.path = path
		self.reloop = reloop
		self.i = 0
		self.begin = 0
		self.end = len(self.path) - 1

	def __str__(self):
		return "Path from {} \n\tto {}".format(self.path[self.begin], self.path[self.end])

	def flip(self):
		self.path.reverse()

	def next(self):
		if self.i >= self.end and self.reloop:
			self.i = self.begin
		if self.i < self.end:
			self.i += 1

	def ended(self):
		return self.i >= self.end

	def go(self):
		return self.path[self.i]

	def then(self):
		if self.i<self.end:
			return self.path[self.i + 1]
		elif self.reloop:
			return self.path[self.begin]

	def overtaked(self,loc):
		return self.go().distance(loc) < self.then().distance(loc)

	def snap(self, loc, near_skip=False):

		for i in range(len(self.path)):
			d = self.path[i].distance(loc)

			if d < self.go().distance(loc):
				self.i = i

		if near_skip: #aim at the next right away
			self.next()

class PathFinder():
	def __init__(self, range = 2500):
		self.range = range

	def selectRange(self, grid, node):
		selected = []

		for n in grid:
			if n.distance(node) < self.range :
				selected.append(n)

		return selected

	def genPath(self, grid, startVec, stopVec):
		nstart = PathFinder.snapVec(grid, startVec)
		nstop = PathFinder.snapVec(grid, stopVec)

		print("genPath")

		nstart.score = 0
		nstart.cost = 0
		nstart.id = 0

		#Dijkstra's algorithm used
		for i in range(len(grid)):
			grid[i].id = i

		for n in grid:
			nbrs = self.selectRange(grid, n)
			for nbr in nbrs:
				if nbr.cost > n.calcCost(nbr):
					nbr.setCost(n)
					nbr.parent = n.i

		return PathFinder.buildPath(grid, nstart, nstop)

	@staticmethod
	def snapVec(grid, vec):
		s_node = grid[0] #set default

		for n in grid:
			d = vec.distance(n.loc)
			if d < vec.distance(s_node.loc):
				s_node = n

		return s_node

	@staticmethod
	def buildPath(grid, nstart, nstop):
		path = []
		nlast = nstop

		print("buildPath")

		while(nlast != nstart):
			path.append(nlast.asTarget())
			nlast = grid[nlast.parent]

		print("endedbuild")
		path.reverse()
		return Path(path,reloop=False)

