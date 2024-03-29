

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
        newBoard = oldboard[:]
        coordinate = self.findCamel(camelNum, oldboard)
        camelTile = oldboard[coordinate[0]]

        #camel picked up plus all above it
        stack = camelTile[ coordinate[1] : ]

        #taking out stack
        newBoard[coordinate[0]] = newBoard[coordinate[0]][:coordinate[1]]

        #moving stack
        newBoard[coordinate[0] + spaces] += stack
        return newBoard

    #takes in the number for the camel to locate. returns coordinate for where the camel is
    def findCamel(self, camelNum, boardstate):
        for i in range(len(boardstate)):
            curTile = boardstate[i]
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
    def chanceCamelWin(self, board):


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
                                ordering1 = ordering + [camelsToChoose1[n]]
                                camelsToChoose2 = camelsToChoose1[:n] + camelsToChoose1[n+1:]

                                for o in range(len(camelsToChoose2)):
                                    ordering2 = ordering1 + [camelsToChoose2[o]]
                                    camelsToChoose3 = camelsToChoose2[:o] + camelsToChoose2[o+1:]

                                    for p in range(len(camelsToChoose3)):
                                        ordering3 = ordering2 + [camelsToChoose3[p]]
                                        camelsToChoose4 = camelsToChoose3[:p] + camelsToChoose3[p+1:]

                                        for q in range(len(camelsToChoose4)):
                                            ordering4 = ordering3 + [camelsToChoose4[q]]
                                            camelsToChoose5 = camelsToChoose4[:q] + camelsToChoose4[q+1:]

                                            for r in range(len(camelsToChoose5)):
                                                ordering5 = ordering4 + [camelsToChoose5[r]]


                                                # by here, ordering should be a list of camel nums that will move the spacings in camelSpacesToMove
                                                #now make the camels move their respective amount

                                                camelNumSpacePairings = []
                                                for a in range(5):
                                                    camelNumSpacePairings += [[ordering5[a], camelSpacesToMove[a][0]]]

                                                newBoardState = Board.deeparraycopy(self, self.appendboxes(board))
                                                for b in range(5):

                                                    newBoardState = self.moveCamel(camelNumSpacePairings[b][0], camelNumSpacePairings[b][1], newBoardState)

                                                # print("final state:", end= '')
                                                # print(newBoardState)
                                                numTimesWin[self.findFrontCamel(newBoardState)-1] += 1
                                                counter += 1
        percentages = [0 for i in range(5)]
        for i in range(5):
            percentages[i] = numTimesWin[i]/counter

        print("initial board is: " + str(board))
        for i in range(len(percentages)):
            print("chance win of " + str(i + 1) + ": " + str(percentages[i]))

    def deeparraycopy(self, array):
        if array == None:
            return None
        retarray = []
        if isinstance(array, int):
            return array
        for i in range(len(array)):
            retarray += [Board.deeparraycopy(self, array[i])]
        return retarray

    def appendboxes(self, array):
        return array + [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

board = Board([[1,2,3,4,5]])
board.chanceCamelWin([[1],[2,3],[4,5]])


