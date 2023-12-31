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
		self.board_score = self.minimax() # we can pre-populate the minimax values

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
		if isGameOver(root):
			return adj  # empty list, means no further possible states

		next = FIRST if getFirst(root) else SECOND
		for i in range(9):
			if (root[i] == BLANK):
				newNode = root[:i] + next + root[i + 1:]
				adj.append(newNode)
			# print(newNode)
		# for i in adj:
		# 	print("/////////")
		# 	print(self.nodeToStr(i))
		return adj


	# returns >0 if 1st player wins, <0 if 2nd player wins, and 0 if tie
	# depth is used so that the AI prioritizes stalling over an immediate loss (this would normally not occur due to the AI being unbeatable)
	def score(self, root, depth):
		match getWinner(root):
			case 1:
				return 10 - depth
			case -1:
				return depth - 10
			case _:
				return 0

	# populates a dict with minimax score values for each board
	def minimax(self, root = None, depth = 0, maximizing=True):
		if (root == None):
			root = self.root
		if (isGameOver(root)):
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
	def printNodes(self, root=None):
		if (root is None):
			root = self.root

		print("current node:\n" + nodeToStr(root) + "\n")
		print("current adjacent node(s):")
		for adj in self.getAdjacentNodes(root):
			print(nodeToStr(adj) + "\n")

# returns a board state in |7|-|9| format
# board goes from          |-|5|-|
# bottom to top            |1|-|3|
def nodeToStr(root=None):
	if (root is None):
		root = "123456789"
	# return root[:3] + "\n" + root[3:6] + "\n" + root[6:9]

	rows = []
	# print in reverse order because i like numpad notation
	for subStr in [root[6:], root[3:6], root[:3]]:
		rows.append("|" + "|".join(subStr) + "|")
	return "\n".join(rows)

# returns true if either a winner exists or all positions are filled, false otherwise
def isGameOver(root):
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

# returns 1 if first player wins, -1 if second player wins, and 0 if a tie occurs
def getWinner(root):
	for line in [[6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
		grid0 = root[line[0]]
		grid1 = root[line[1]]
		grid2 = root[line[2]]

		if (grid0 != BLANK):
			if (grid0 == grid1 and grid1 == grid2):
				return 1 if grid0 == FIRST else -1
	return 0 # on tie

class AI:
	def __init__(self, game):
		self.game = game # GameGraph
		self.board_score = game.board_score

	# returns node/string representing best next board state for AI
	def turn(self, root):
		moves = {}
		adj_nodes = self.game.getAdjacentNodes(root)
		if (len(adj_nodes) == 0):
			return root
		for next in adj_nodes:
			moves[next] = self.board_score[next]

		# pick max if AI is playing for P1 slot, min otherwise
		first = getFirst(root)
		if (first): return max(moves, key=moves.get)
		return min(moves, key=moves.get)

# returns 1 if P1 is next to make a move, 0 otherwise
def getFirst(root):
	return root.count(BLANK) % 2

class LiveGame:
	def __init__(self, game, userFirst = True):
		self.game = game # GameGraph
		self.userFirst = userFirst
		self.board = self.game.root
		self.opponent = AI(self.game)

	def playerTurn(self):
		next = FIRST if getFirst(self.board) else SECOND
		adj_nodes = self.game.getAdjacentNodes(self.board)
		index = int(input("Input your next position: [1-9]\nYour turn: ")) - 1
		newBoard = self.board[:index] + next + self.board[index + 1:]
		if (newBoard not in adj_nodes):
			print("Invalid move")
			return False # error
		self.board = newBoard
		return True

	def gameLoop(self):
		print(nodeToStr())
		# AI first turn if human not first
		if (not self.userFirst):
			self.board = self.opponent.turn(self.board)
			print("AI turn: \n" + nodeToStr(self.board))

		gameOver = isGameOver(self.board)
		while(not gameOver):
			isValid = self.playerTurn()
			while(not isValid):
				isValid = self.playerTurn()
			print(nodeToStr(self.board))
			gameOver = isGameOver(self.board)
			if (gameOver): break # this will never be used because the AI cannot lose

			self.board = self.opponent.turn(self.board)
			print("AI turn: \n" + nodeToStr(self.board))
			gameOver = isGameOver(self.board)

		winner = getWinner(self.board)
		result = "Nobody WINS"
		match winner:
			case 1: result = f"Player {FIRST} WINS"
			case -1: result = f"Player {SECOND} WINS"
 
		print(result)
		print("Final board: ")
		print(nodeToStr(self.board))


board = GameGraph()
with open('output.json', 'w+') as f:
	json.dump(board.nodes, f, indent="\t")

#
# opponent = AI(board)
# print(nodeToStr() + "\n")
#
# testNode = "o---x--xo"
# state = EMPTYBOARD
# # state = "----o----"
# # state = testNode
# print(nodeToStr(state) + "\n")
# while (not isGameOver(state)):
# 	state = opponent.turn(state)
# 	print(nodeToStr(state) + "\n")

userMark = input("Pick a side: \n" +
				 "Input \'" + FIRST + "\' to go first\n" +
				 "Input \'" + SECOND + "\' to go second\n")
game = LiveGame(board, userMark == FIRST)
game.gameLoop()