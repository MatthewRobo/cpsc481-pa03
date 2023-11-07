# implementation by Matthew Nguyen
# CWID: 872515754

import json

first = "o"
second = "x"
blank = "-"

class GameGraph:
	def __init__(self, root = None):
		self.root = root
		if (root is None):
			self.root = blank * 9 # "---------", blank board
		self.nodes = {self.root:[]} # dict of key=board state and values=child (future) states of board
	
	# adds nodes and adjacent nodes to the graph
	def addNode(self, root, adj): 
		self.nodes[root] = adj;
		return
	
	def getAdjacentNodes(self, root):
		return self.nodes[root]
	
	# generates all child states of the chosen board state
	# if no parameters, generates every possible legal state
	# based off DFS algorithm
	def generateTree(self, root = None): 
		if (root is None):
			root = self.root
		
		self.addNode(root, self.generateAdjacentNodes(root))
		for adj in self.nodes[root]:
			self.generateTree(adj)
		
		return
	
	# generates all possible next moves of chosen board state
	# returns list of next board states
	def generateAdjacentNodes(self, root):
		adj = []
		if self.isGameOver(root):
			return adj # empty list, means no further possible states
		
		next = second if (root.count(first) > root.count(second)) else first
		for i in range(9):
			if (root[i] == blank):
				newNode = root[:i] + next + root[i+1:]
				adj.append(newNode)
				# print(newNode)
		# for i in adj:
		# 	print("/////////")
		# 	print(self.nodeToStr(i))
		return adj
	
	# returns true if either a winner exists or all positions are filled, false otherwise
	def isGameOver(self, root):
		if (blank not in root):
			return True
		
		for line in [[6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
			grid0 = root[line[0]]
			grid1 = root[line[1]]
			grid2 = root[line[2]]
			
			if (grid0 != blank):
				if (grid0 == grid1 and grid1 == grid2):
					return True
			
		return False
	
	# returns a board state in |-|-|-| format
	#                          |-|-|-|
	#                          |-|-|-|
	def nodeToStr(self, root=None):
		if (root is None):
			root = self.root
		# return root[:3] + "\n" + root[3:6] + "\n" + root[6:9]
		
		rows = []
		for subStr in [root[:3], root[3:6], root[6:]]:
			rows.append("|" + "|".join(subStr) + "|")
		return "\n".join(rows)
	
	# prints chosen board state and immediate future board states
	def printNode(self, root=None):
		if (root is None):
			root = self.root
		
		print("current node:\n" + self.nodeToStr(root) + "\n")
		print("current adjacent node(s):")
		for adj in self.getAdjacentNodes(root):
			print(self.nodeToStr(adj) + "\n")
	
board = GameGraph()

board.generateAdjacentNodes(board.root)
board.generateTree()

board.printNode("-xx-o-oox")
print(len(board.nodes))

with open('output.json', 'w+') as f:
	json.dump(board.nodes, f, indent="\t") 
	# i HATE space indent
	# yes this is important enough to dedicate two lines to
