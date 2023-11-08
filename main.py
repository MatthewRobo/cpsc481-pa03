# implementation by Matthew Nguyen
# CWID: 872515754

import json

FIRST = "o"
SECOND = "x"
BLANK = "-"

EMPTYBOARD = BLANK * 9

class GameGraph:
	def __init__(self):
		self.root = BLANK * 9  # "---------", blank board
		self.nodes = {self.root: []}  # dict of key=board state and values=child (future) states of board
		self.generateTree()
		self.board_score = self.minimax()

	# adds nodes and adjacent nodes to the graph
	def addNode(self, root, adj):
		self.nodes[root] = adj
		return

	def getAdjacentNodes(self, root):
		return self.nodes[root]

	# generates all child states of the chosen board state
	# if no parameters, generates every possible legal state
	# based off DFS algorithm
	def generateTree(self, root=None):
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
			return adj  # empty list, means no further possible states

		next = SECOND if (root.count(FIRST) > root.count(SECOND)) else FIRST
		for i in range(9):
			if (root[i] == BLANK):
				newNode = root[:i] + next + root[i + 1:]
				adj.append(newNode)
			# print(newNode)
		# for i in adj:
		# 	print("/////////")
		# 	print(self.nodeToStr(i))
		return adj

	# returns true if either a winner exists or all positions are filled, false otherwise
	def isGameOver(self, root):
		# checks to see if board is filled
		if (BLANK not in root):
			return True

		# checks to see if board has three-in-row
		for line in [[6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
			grid0 = root[line[0]]
			grid1 = root[line[1]]
			grid2 = root[line[2]]

			if (grid0 != BLANK):
				if (grid0 == grid1 and grid1 == grid2):
					return True
		return False

	def getWinner(self, root):
		for line in [[6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
			grid0 = root[line[0]]
			grid1 = root[line[1]]
			grid2 = root[line[2]]

			if (grid0 != BLANK):
				if (grid0 == grid1 and grid1 == grid2):
					return 1 if grid0 == FIRST else -1
		return 0 # on tie

	def score(self, root, depth):
		match self.getWinner(root):
			case 1:
				return 10 - depth
			case -1:
				return depth - 10
			case _:
				return 0

	def minimax(self, root = None, depth = 0, maximizing=True):
		if (root == None):
			root = self.root
		if (self.isGameOver(root)):
			return {root: self.score(root, depth)}

		depth += 1
		board_score = {}  # KV pairs of gamestate - score

		adj_moves = self.getAdjacentNodes(root)
		for adj_node in adj_moves:
			board_score.update(self.minimax(adj_node, depth, not maximizing))

		if maximizing:
			board_score[root] = max(board_score.values())
		else:
			board_score[root] = min(board_score.values())


		return board_score

	# prints chosen board state and immediate future board states
	def printNode(self, root=None):
		if (root is None):
			root = self.root

		print("current node:\n" + nodeToStr(root) + "\n")
		print("current adjacent node(s):")
		for adj in self.getAdjacentNodes(root):
			print(nodeToStr(adj) + "\n")

# returns a board state in |-|-|-| format
#                          |-|-|-|
#                          |-|-|-|
def nodeToStr(root=None):
	if (root is None):
		root = "123456789"
	# return root[:3] + "\n" + root[3:6] + "\n" + root[6:9]

	rows = []
	# print in reverse order because i like numpad notation
	for subStr in [root[6:], root[3:6], root[:3]]:
		rows.append("|" + "|".join(subStr) + "|")
	return "\n".join(rows)


class AI:
	def __init__(self, first, game):
		self.first = first # bool
		self.game = game # GameGraph
		self.board_score = game.board_score

	# returns node/string representing best board state for AI
	def turn(self, root):
		moves = {}
		adj_nodes = self.game.getAdjacentNodes(root)
		if (len(adj_nodes) == 0):
			return "ENDENDEND"
		# print(">>>")
		for next in adj_nodes:
			moves[next] = self.board_score[next]

			# print(nodeToStr(next))
			# print(self.board_score[next])

		# print("<<<")
		if (self.first): return max(moves, key=moves.get)
		return min(moves, key=moves.get)





board = GameGraph()


computer = AI(True, board)
testNode = "o---x--xo"
print(nodeToStr() + "\n")


computer2 = AI(False, board)

# state = EMPTYBOARD
# state = "----o----"
state = testNode
print(nodeToStr(state) + "\n")
while (state != "ENDENDEND"):

	state = computer.turn(state)
	print(nodeToStr(state) + "\n")
	state = computer2.turn(state)
	print(nodeToStr(state) + "\n")

# state = "----o----"
# print(nodeToStr(state) + "\n")
# while (state != "ENDENDEND"):
#
# 	state = computer2.turn(state)
# 	print(nodeToStr(state) + "\n")
# 	state = computer.turn(state)
# 	print(nodeToStr(state) + "\n")
with open('output.json', 'w+') as f:
	json.dump(board.nodes, f, indent="\t")



