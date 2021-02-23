import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent

MAX = 1000000000000000
FOUR = 100000
BLOCK_FOUR = 10000
THREE = 5000
BLOCK_THREE = 1670
TWO = 1500
BLOCK_TWO = 300
MIN = 0


#   @return:
#   int giving the distance between two points
def distance(point1, point2):
    changeX = point2[0] - point1[0]
    # - If distance between points is negative
    if changeX < 0:
        changeX = changeX * - 1

    changeY = point2[1] - point1[1]
    if changeY < 0:
        changeY = changeY * - 1

    return np.sqrt((changeX ** 2) + (changeY ** 2))


#   @return:
#   int given the centroid of a player's points
def centroid(playerId, board):
    """ - Requires use of the total x coordinates, y coordinate, and the amount of points to calculate a mean value for
    the centroid x and y """
    totalX = 0
    totalY = 0
    totalPoints = 0

    BOARD_SIZE = board.shape[0]

    # = Goes through the board getting all points
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[(x, y)] == playerId:
                totalX = totalX + x
                totalY = totalY + y
                totalPoints = totalPoints + 1

    # - Returns mean x value and y value, if 0 points just returns center
    if totalPoints == 0:
        return BOARD_SIZE / 2, BOARD_SIZE / 2
    return (totalX / totalPoints), (totalY / totalPoints)


#   @return:
#   int giving number of empty spaces at ends of line for diagonals
def endTestDiag(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):

            emptyEnds = 0
            if legalMove(board, (r - 1, c - 1)):
                emptyEnds += 1
            if legalMove(board, (r + X_IN_A_LINE, c + X_IN_A_LINE)):
                emptyEnds += 1

            flag = True
            for i in range(X_IN_A_LINE):
                if board[r + i, c + i] != playerID:
                    flag = False
                    break
            if flag:
                return emptyEnds
    return 0


#   @return:
#   int giving number of empty spaces at ends of line for rows
def endTestRow(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):

            emptyEnds = 0
            if legalMove(board, (r, c - 1)):
                emptyEnds += 1
            if legalMove(board, (r, c + X_IN_A_LINE)):
                emptyEnds += 1

            flag = True
            for i in range(X_IN_A_LINE):
                if board[r, c + i] != playerID:
                    flag = False
                    break
            if flag:
                return emptyEnds
    return 0


class Player(GomokuAgent):
    def move(self, board):
        """ Initalize the reward board, used to determine best move, the maximum distance between points and the center
        of player points """
        rewards = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        maxDistance = distance((0, 0), (self.BOARD_SIZE, self.BOARD_SIZE))
        center = centroid(self.ID, board)

        # - For every location in the board (x coordinate and y coordinate)
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                # - Generates a tuple of the possible move
                moveLoc = (x, y)

                # - Checks if the move is legal on the current board
                if legalMove(board, moveLoc):
                    ''' - Sets the base value of the reward to the max distance subtract the distance between the move 
                    and center '''
                    rewards[moveLoc] = maxDistance - distance(moveLoc, center)

                    ''' Copies the board and sets the copy board move location to the player's id
                    (Marks the player's move as the current location on the copy board) '''
                    copyBoard = copy.deepcopy(board)
                    copyBoard[moveLoc] = self.ID

                    # - If the player has a winning move play that winning move
                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE):
                        return moveLoc

                    ''' - If the other player has a winning move block that move, we do x in a line -2 first to
                    check if they have a checkmate type move (Imagine that a player needs to get 5 in a row if
                    they have 3 in a row with both sides open they can place on one either side to get the win)'''
                    copyBoard[moveLoc] = self.ID * -1

                    # - If the enemy has a winning move prioritise blocking that winning move
                    if winningTest(self.ID * -1, copyBoard, self.X_IN_A_LINE):
                        rewards[moveLoc] = rewards[moveLoc] + MAX

                    # - If the player can get 4 in a row with 2 empty spaces
                    copyBoard[moveLoc] = self.ID
                    if diagTest(self.ID, copyBoard, self.X_IN_A_LINE - 1) and \
                            endTestDiag(self.ID, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + FOUR

                    if rowTest(self.ID, copyBoard, self.X_IN_A_LINE - 1) and \
                            endTestRow(self.ID, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + FOUR

                    ''' If the enemy can get 3 in a row/diagonal angle we want to block them from getting 4 if there
                    are two empty spaces '''
                    copyBoard[moveLoc] = self.ID * -1
                    if diagTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) and \
                            endTestDiag(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_FOUR

                    if rowTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) and \
                            endTestRow(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_FOUR

                    # - If the player can get 3 in a row with 2 empty spaces
                    copyBoard[moveLoc] = self.ID
                    if diagTest(self.ID, copyBoard, self.X_IN_A_LINE - 2) and \
                            endTestDiag(self.ID, copyBoard, self.X_IN_A_LINE - 2) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + THREE

                    if rowTest(self.ID, copyBoard, self.X_IN_A_LINE - 2) and \
                            endTestRow(self.ID, copyBoard, self.X_IN_A_LINE - 2) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + THREE

                    ''' If the enemy can get 2 in a row/diagonal angle we want to block them from getting 3 if there
                        are two empty spaces '''
                    copyBoard[moveLoc] = self.ID * -1
                    if diagTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 2) and \
                            endTestDiag(self.ID * -1, copyBoard, self.X_IN_A_LINE - 2) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_FOUR

                    if rowTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 2) and \
                            endTestRow(self.ID * -1, copyBoard, self.X_IN_A_LINE - 2) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_THREE

                    # - If the player can get 2 in a row with 2 empty spaces
                    copyBoard[moveLoc] = self.ID
                    if diagTest(self.ID, copyBoard, self.X_IN_A_LINE - 3) and \
                            endTestDiag(self.ID, copyBoard, self.X_IN_A_LINE - 3) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + TWO

                    if rowTest(self.ID, copyBoard, self.X_IN_A_LINE - 3) and \
                            endTestRow(self.ID, copyBoard, self.X_IN_A_LINE - 3) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + TWO

                    ''' If the enemy can get 1 in a row/diagonal angle we want to block them from getting 2 if there
                        are two empty spaces '''
                    copyBoard[moveLoc] = self.ID * -1
                    if diagTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 3) and \
                            endTestDiag(self.ID * -1, copyBoard, self.X_IN_A_LINE - 3) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_TWO

                    if rowTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 3) and \
                            endTestRow(self.ID * -1, copyBoard, self.X_IN_A_LINE - 3) > 1:
                        rewards[moveLoc] = rewards[moveLoc] + BLOCK_TWO

        # Takes the best action that the AI found
        bestReward = 0
        bestMove = (0, 0)
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if rewards[(i, j)] > bestReward:
                    bestMove = (i, j)
                    bestReward = rewards[(i, j)]

        return bestMove
