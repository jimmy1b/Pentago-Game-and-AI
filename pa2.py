import random
# TILES = 4
# SPACES = 9
# board = [[[]for i in range(SPACES)] for j in range(TILES)]

board = [[['.' for i in range(3)] for j in range(3)] for k in range(4)]
pl = ""
computer = ""
out = open("Output.txt", "w")

def boardPrint(gameboard):
	a = "+-------+-------+"
	for i in range(6):
		if i == 3:
			a += str("\n+-------+-------+")
		a += str("\n| ")
		for j in range(2):
			for k in range(3):
				# print '.'
				a += str(gameboard[j + 2 * (i / 3)][i % 3][k])
				a += " "

			a += str("| ")
	a += str("\n+-------+-------+\n")
	print a
	out.write(a)


def boardClear(gameboard):
	for i in range(4):
		for j in range(3):
			for k in range (3):
				gameboard[i][j][k] = '.'

def place(gameboard, block, space, player):
	gameboard[block - 1][(space - 1) / 3][(space - 1) % 3] = player

def isOpenSpace(gameboard, block, space):
	if gameboard[block - 1][(space - 1) / 3][(space - 1) % 3] == '.':
		return True
	else:
		return False #space in use

def isBoardFull(gameboard):
	for i in range(4):
		for j in range(3):
			for k in range (3):
				if gameboard[i][j][k] == '.':
					return False

	return True

def turnL(gameboard, block):
	if block < 1 or block > 4:
		return None

	# print block, 'L'
	new = [['.' for i in range(3)] for j in range(3)]
	k =0
	for i in range(2, -1, -1):
		for j in range(3):
			# print i, j, k
			new[k][j] = gameboard[block - 1][j][i]

		k = (k + 1) % 3

	return new

def turnR(gameboard, block):
	if block < 1 or block > 4:
		return None

	# print block, 'R'
	new = [['.' for i in range(3)] for j in range(3)]
	k =0
	for i in range(3):
		for j in range(2, -1, -1):
			# print i, j, k
			new[i][k] = gameboard[block - 1][j][i]
			k = (k + 1) % 3

	# for i in range(3):
	# 	for j in range(3): 
	# 		print i, j, new[i][j]
	# 		gameboard[block-1][i][j] = new[i][j]
	# 		print gameboard[block-1][i][j], block, i, j
	return new

#checks for any 5 in a row on the gameboard, given the player
def checkWin(gameboard, player):

	return checkH(board, player) or checkV(board, player) or checkDdn(board, player) or checkDup(board, player)

#checks for 5 in a row, horizontal
def checkH(gameboard, player):
	for i in range(2):
		for j in range(6):
			block = i * 2
			row = j / 2
			column = j % 2
			for k in range(5):
				# print gameboard[block][row][column]
				if gameboard[block][row][column] == player:
					if k == 4:
						return True
					column = (column + 1) % 3
					if column == 0:
						block += 1
				else:
					# print
					break

	return False


#checks for 5 in a row, vertical
def checkV(gameboard, player):
	for i in range(2):
		for j in range(6):
			block = i
			row = j % 2
			column = j / 2
			for k in range(5):
				# print gameboard[block][row][column], block, row, column
				if gameboard[block][row][column] == player:
					if k == 4:
						return True
					row = (row + 1) % 3
					if row == 0:
						block += 2
				else:
					# print
					break

	return False

#checks for 5 in a row, diagonal down
def checkDdn(gameboard, player):
	for j in range(4):
		block = 0
		row = j / 2
		column = j % 2
		for k in range(5):
			# print gameboard[block][row][column], block, row, column, 'k', k
			if gameboard[block][row][column] == player:
				if k == 4:
					return True
				row = (row + 1) % 3
				column = (column + 1) % 3
				if row == 0 and column == 0:
					block = 3
				elif row == 0:
					if k == 1:
						block = 2
					else:
						block = 3
				elif column == 0:
					if k == 1:
						block = 1
					else:
						block = 3
			else:
				# print
				break

	return False

#checks for 5 in a row, diagonal up
def checkDup(gameboard, player):
	for j in range(4):
		block = 2
		row = 2 - j / 2
		column = j % 2
		for k in range(5):
			# print gameboard[block][row][column], block, row, column, 'k', k
			if gameboard[block][row][column] == player:
				if k == 4:
					return True
				row = (row - 1) % 3
				column = (column + 1) % 3
				if row == 2 and column == 0:
					block = 1
				elif row == 2:
					if k == 1:
						block = 0
					else:
						block = 1
				elif column == 0:
					if k == 1:
						block = 3
					else:
						block = 1
			else:
				# print
				break

	return False


def getMoves(gameboard):
	moves = set()
	for i in range(4):
		for j in range(3):
			for k in range(3):
				for l in range(4):
					if isOpenSpace(gameboard, i + 1, j * 3 + k + 1) == True:
						moves.add("%d%d%dl" % (i + 1, j * 3 + k + 1, l + 1))
						moves.add("%d%d%dr" % (i + 1, j * 3 + k + 1, l + 1))
	# print len(moves)
	return moves

def heuristic(gameboard, player):
	#+1 for every possible win condition
	#+100 for a winning leaf
	#-1 for opponent win condition
	#-100 for losing leaf
	opponent = ""
	if player == "w":
		opponent = "b"
	else:
		opponent = "w"

	score = 0
	score += checkWinConditions(gameboard, player)
	score -= checkWinConditions(gameboard, opponent)
	if checkWin(gameboard, player) == True:
		score += 100
	if checkWin(gameboard, opponent) == True:
		score -= 100
	return score

def checkWinConditions(gameboard, player):
	count = checkHCon(gameboard, player) + checkVCon(gameboard, player) + checkDdnCon(gameboard, player) + checkDupCon(gameboard, player)
	return count


def checkHCon(gameboard, player):
	count = 0
	for i in range(2):
		for j in range(6):
			found = False
			block = i * 2
			row = j / 2
			column = j % 2
			for k in range(5):
				# print gameboard[block][row][column]
				if gameboard[block][row][column] == player:
					found = True
				elif gameboard[block][row][column] != ".":
					break

				column = (column + 1) % 3
				if column == 0:
					block += 1

				if k == 4 and found == True:
					count += 1

	return count

def checkVCon(gameboard, player):
	count = 0
	for i in range(2):
		for j in range(6):
			found = False
			block = i
			row = j % 2
			column = j / 2
			for k in range(5):
				# print gameboard[block][row][column], block, row, column
				if gameboard[block][row][column] == player:
					found = True
				elif gameboard[block][row][column] != ".":
					break

				row = (row + 1) % 3
				if row == 0:
					block += 2

				if k == 4 and found == True:
					count += 1

	return count

def checkDdnCon(gameboard, player):
	count = 0
	for j in range(4):
		found = False
		block = 0
		row = j / 2
		column = j % 2
		for k in range(5):
			# print gameboard[block][row][column], block, row, column, 'k', k
			if gameboard[block][row][column] == player:
				found = True
			elif gameboard[block][row][column] != ".":
				break

			row = (row + 1) % 3
			column = (column + 1) % 3
			if row == 0 and column == 0:
				block = 3
			elif row == 0:
				if k == 1:
					block = 2
				else:
					block = 3
			elif column == 0:
				if k == 1:
					block = 1
				else:
					block = 3

			if k == 4 and found == True:
					count += 1

	return count

def checkDupCon(gameboard, player):
	count = 0
	for j in range(4):
		found = False
		block = 2
		row = 2 - j / 2
		column = j % 2
		for k in range(5):
			# print gameboard[block][row][column], block, row, column, 'k', k
			if gameboard[block][row][column] == player:
				found = True
			elif gameboard[block][row][column] != ".":
				break

			row = (row - 1) % 3
			column = (column + 1) % 3
			if row == 2 and column == 0:
				block = 1
			elif row == 2:
				if k == 1:
					block = 0
				else:
					block = 1
			elif column == 0:
				if k == 1:
					block = 3
				else:
					block = 1

			if k == 4 and found == True:
					count += 1

	return count

def undo(gameboard, move):
	if move[3] == "l":
		gameboard[int(move[2]) - 1] = turnR(gameboard, int(move[2]))
	elif move[3] == "r":
		gameboard[int(move[2]) - 1] = turnL(gameboard, int(move[2]))
	place(gameboard, int(move[0]), int(move[1]), '.')

def minMax(alpha, beta, depth, gameboard, isMax, prune):
	if depth == 0 or isBoardFull(gameboard) == True or checkWin(gameboard, computer) == True or checkWin(gameboard, pl) == True: 
		return (None, heuristic(gameboard, computer), 1)
	moves = getMoves(gameboard)
	# print len(moves)

	if isMax == True:
		best = None
		expanded = 1
		for move in moves:
			place(gameboard, int(move[0]), int(move[1]), computer)
			if checkWin(gameboard, pl) == False:
				if move[3] == "l":
					gameboard[int(move[2]) - 1] = turnL(gameboard, int(move[2]))
				else:
					gameboard[int(move[2]) - 1] = turnR(gameboard, int(move[2]))
				nextMove = minMax(alpha, beta, depth - 1, gameboard, not isMax, prune)
				undo(gameboard, move)
			else:
				nextMove = minMax(alpha, beta, depth - 1, gameboard, not isMax, prune)
				undo(gameboard, str(move[0] + move[1] + "  "))
			expanded += nextMove[2]
			if best == None or best[1] < nextMove[1]:
				best = (move, nextMove[1], expanded)
			if prune == True:
				if best[1] > alpha:
					alpha = best[1]
				if beta <= alpha:
					return (None, alpha, expanded)
		return (best[0], best[1], expanded)
	else:
		best = None
		expanded = 1
		for move in moves:
			place(gameboard, int(move[0]), int(move[1]), pl)
			if checkWin(gameboard, pl) == False:
				if move[3] == "l":
					gameboard[int(move[2]) - 1] = turnL(gameboard, int(move[2]))
				else:
					gameboard[int(move[2]) - 1] = turnR(gameboard, int(move[2]))
				nextMove = minMax(alpha, beta, depth - 1, gameboard, not isMax, prune)
				undo(gameboard, move)
			else:
				nextMove = minMax(alpha, beta, depth - 1, gameboard, not isMax, prune)
				undo(gameboard, str(move[0] + move[1] + "  "))
			expanded += nextMove[2]
			if best == None or best[1] > nextMove[1]:
				best = (move, nextMove[1], expanded)
			if prune == True:
				if best[1] < beta:
					beta = best[1]
				if beta <= alpha:
					return (None, beta, expanded)
		return (best[0], best[1], expanded)


#---------------------------------------------------------------------------------------------------------------------------
#Running Game

# print minMax(float("-inf"), float("inf"), 2, board, True, True)

# place(board, 4, 2, 'w')
# board[1] = turnR(board, 2)

# boardPrint(board)

# print heuristic(board, computer)
# boardClear(board)

boardPrint(board)

while pl != "w" and pl != "b":
	pl =  raw_input("What color do you want to play as? (w/b): ").lower()
	out.write(str("What color do you want to play as? (w/b): " + pl))

if pl == 'w':
	computer = "b"

else:
	computer = "w"


first = " "
while first != "y" and first != "n" and first[0] != "r":
	first = raw_input("Do you want to go first? (y/n/random): ").lower()
	out.write(str("Do you want to go first? (y/n/random): " + first))

if first == "y":
	current = "p"

elif first == "n":
	current = "a"

else:
	if random.randint(0,1) == 1:
		current = "p"
	else:
		current = "a"

print
out.write("\n")
done = False
tie = False
winner = "none"
while done == False:

	if current == "p":
		correct = False
		move = ""
		print "Move format: b/p bd \nb = block\np = position in block\nd = direction to rotate the block (\"L\", \"R\")\n"
		out.write("Move format: b/p bd \nb = block\np = position in block\nd = direction to rotate the block (\"L\", \"R\")\n")
		b1 = ""
		p = ""
		b2 = ""
		d = ""
		while correct == False:
			move = raw_input("Make your move(%s): " % (pl)).lower()
			out.write(str("Make your move(" + pl + "): " + move))
			if len(move) < 6:
				b1 = "a"
			else:
				b1 = move[0]
				p = move[2]
				b2 = move[4]
				d = move[5]
			correct = b1.isdigit() and p.isdigit() and b2.isdigit() and int(b1) > 0 and int(b1) < 5 \
						and int(p) > 0 and int(p) < 10 and int(b2) > 0 and int(b2) < 5 \
						and (d == "l" or d == "r") and isOpenSpace(board, int(b1), int(p))

		# print b1, "/", p, " ", b2, d
		place(board, int(b1), int(p), pl)
		done = checkWin(board, pl)
		if done == True:
			winner = pl
			print
			out.write("\n")
			boardPrint(board)
			print str("(You) " + pl + ": " + move[:3].upper())
			out.write(str("(You) " + pl + ": " + move[:3].upper()))
			print
			out.write("\n")
			break

		if d == "l":
			board[int(b2) - 1] = turnL(board, int(b2))
		else:
			board[int(b2) - 1] = turnR(board, int(b2))
			
		tie = checkWin(board, pl) and checkWin(board, computer)
		done = checkWin(board, pl)
		if tie == True:
			done = True

		if done == True:
			winner = pl

		print
		out.write("\n")
		boardPrint(board)
		print str("(You) " + pl + ": " + move.upper())
		out.write(str("(You) " + pl + ": " + move.upper()))
		print
		out.write("\n")
		if done == False:
			current = "a"

	else:
		#call computer for next move
		depth = 2 #starts running slow with a lookahead of 3 or greater
		pruning = True #runs a lot slower without alpha beta pruning
		move = minMax(float("-inf"), float("inf"), depth, board, True, pruning)[0]
		#check win on place
		place(board, int(move[0]), int(move[1]), computer)
		done = checkWin(board, computer)
		if done == True:
			winner = computer
			print
			out.write("\n")
			boardPrint(board)
			print str("(ai) " + computer + ": " + move[0] + "/" + move[1])
			out.write(str("(ai) " + computer + ": " + move[0] + "/" + move[1]))
			print
			out.write("\n")
			break
		#check win on turn
		if move[3] == "l":
			board[int(move[2]) - 1] = turnL(board, int(move[2]))
		else:
			board[int(move[2]) - 1] = turnR(board, int(move[2]))
			
		tie = checkWin(board, pl) and checkWin(board, computer)
		done = checkWin(board, computer)
		if tie == True:
			done = True

		if done == True:
			winner = computer

		print
		out.write("\n")
		boardPrint(board)
		print str("(ai) " + computer + ": " + move[0] + "/" + move[1] + " " + move[2] + move[3].upper())
		out.write(str("(ai) " + computer + ": " + move[0] + "/" + move[1] + " " + move[2] + move[3].upper()))
		print
		out.write("\n")
		print
		out.write("\n")
		if done == False:
			current = "p"

if tie == False:
	print str("winner: (" + current + ") " + winner)
	out.write(str("winner: (" + current + ") " + winner))
else:
	print "tie"
	out.write("tie")
out.close()