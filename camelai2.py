class Game(object):
	def __init_(self, boardstate):
		self.board = Board(boardstate) #2d array of camel and thier places [[],[], [], [] ,[] ]
		self.camels = [Camels(1),Camels(2),Camels(3),Camels(4),Camels(5)]




""" [[1,3], [], [2], [4,5], [], [], []]
	moveCamel(3,1)
	return [[1], [3], [2], [4,5]]

	moveCamel(1,1)
	return [[], [1, 3], [2], [4,5]]

	moveCamel(2,1)
	return [[1], [3], [], [4,5,2]]

	[1 ,2] + [3] = [1, 2, 3]

[0,1,2,3,4]
[startind : endind : spacing]

"""
class Board(object):
	def __init__(self, boardstate):
	    self.boardstate = boardstate #2d array

    def moveCamel(self, camelNum, spaces, oldboard):
        print(oldboard)
        newboard = oldboard[:]
        coordinate = self.findCamel(camelNum)
        print(coordinate[0])
        print(oldboard(coordinate[0])
        camelTile = oldboard[coordinate[0]]

        #camel picked up plus all above it
        stack = camelTile[ coordinate[1] : ]

        #taking out stack
        newBoard[coordinate[0]] = newBoard[coordinate[0]][:coordinate[1]]

        #moving stack
        newBoard[coordinate[0] + spaces] += stack

        return newBoard

	#takes in the number for the camel to locate. returns coordinate for where the camel is
	def findCamel(self, camelNum):
		for i in range(len(self.boardstate)):
			curTile = self.boardstate[i]
			for j in range(len(curTile)): #[[], [camel1, camel2], [],[]]
				curCamel = curTile[j]
				if curCamel == camelNum:
					return [i,j]

	#returns the camelNum that is in front
	def findFrontCamel(self, board):
		for i in range(len(board)-1, -1, -1):
			curTile = board[i]
			if curTile != []:
				return curTile[-1]



	#assign all possible spaces to move for every camel, then assign the order to move camels, then run boardstate accordinly, then see if specific camel is in front.
	#[[3,1],[2,2],[5,1],[4,1],[1,1]]
	def chanceCamelWin(self, camelCheckWin):

		numTimesWin = [0,0,0,0,0]
		counter = 0
		#assign all possible spaces to move for every camel
		for i in range(1,4):
			for j in range(1,4):
				for k in range(1,4):
					for l in range(1,4):
						for m in range(1,4):
							camelSpacesToMove = [[i],[j],[k],[l],[m]]


							#then assign the order to move camels
							camelsToChoose1 = [1,2,3,4,5]
							ordering = []
							for n in range(len(camelsToChoose1)):
								ordering = ordering + [camelsToChoose1[n]]
								camelsToChoose2 = camelsToChoose1[:n] + camelsToChoose1[n+1:]

								for o in range(len(camelsToChoose2)):
									ordering = ordering + [camelsToChoose2[o]]
									camelsToChoose3 = camelsToChoose1[:o] + camelsToChoose1[o+1:]

									for p in range(len(camelsToChoose3)):
										ordering = ordering + [camelsToChoose3[p]]
										camelsToChoose4 = camelsToChoose1[:p] + camelsToChoose1[p+1:]

										for q in range(len(camelsToChoose4)):
											ordering = ordering + [camelsToChoose4[q]]
											camelsToChoose5 = camelsToChoose1[:q] + camelsToChoose1[q+1:]

											for r in range(len(camelsToChoose5)):
												ordering = ordering + [camelsToChoose5[r]]


												# by here, ordering should be a list of camel nums that will move the spacings in camelSpacesToMove
												#now make the camels move their respective amount

												camelNumSpacePairings = []
												for a in range(5):
													camelNumSpacePairings += [[ordering[a], camelSpacesToMove[a]]]

												newBoardState = self.boardstate[:]
												for b in range(5):
													newBoardState = self.moveCamel(camelNumSpacePairings[0], camelNumSpacePairings[1], newBoardState)

												numTimesWin[self.findFrontCamel(newBoardState)-1] += 1
												counter += 1
		percentages = []
		for i in range(5):
			percentages[i] = numTimesWin[i]/counter

		print(percentages)



def testfunc():
        print("working")

board = Board([[1,2,3,4,5],[],[],[]])
board.chanceCamelWin(1)
