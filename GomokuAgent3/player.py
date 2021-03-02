import numpy as np
import copy

from misc import legalMove, diagTest, rowTest, winningTest
from gomokuAgent import GomokuAgent
import gomokuAgent


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


def rewardAtPoint(ID, board, X_IN_A_LINE, point):
    copyBoard = copy.deepcopy(board)
    reward1 = rewardAtPointAux(ID, copyBoard, X_IN_A_LINE, point)

    copyBoardPrime = copy.deepcopy(board)
    copyBoardPrime = np.rot90(copyBoardPrime)
    pointPrime = (len(board) - 1 - point[1], point[0])
    reward2 = rewardAtPointAux(ID, copyBoardPrime, X_IN_A_LINE, pointPrime)

    return reward1 + reward2


def rewardAtPointAux(ID, copyBoard, X_IN_A_LINE, point):
    """ - Sets the base value of the reward to the max distance subtract the distance between the move
        and center """
    maxDistance = distance((0, 0), (copyBoard.shape[0], copyBoard.shape[0]))
    center = centroid(ID, copyBoard)
    reward = maxDistance - distance(point, center)
    copyBoard[point] = ID
    rewardIncremental = maxDistance * 2

    for x in range(0, X_IN_A_LINE + 1):
        # - If the player can get 2 in a row with 2 empty spaces
        copyBoard[point] = ID * - 1

        if diagTest(ID * - 1, copyBoard, x) and \
                endTestDiag(ID * - 1, copyBoard, x) > 1:
            reward = reward + rewardIncremental

        if rowTest(ID * - 1, copyBoard, x) and \
                endTestRow(ID * - 1, copyBoard, x) > 1:
            reward = reward + rewardIncremental

        rewardIncremental = 2 * (rewardIncremental ** 2)
        ''' If the enemy can get 1 in a row/diagonal angle we want to block them from getting 2 if there
            are two empty spaces '''
        copyBoard[point] = ID

        if diagTest(ID, copyBoard, x) and \
                endTestDiag(ID, copyBoard, x) > 1:
            reward = reward + rewardIncremental

        if rowTest(ID, copyBoard, x) and \
                endTestRow(ID, copyBoard, x) > 1:
            reward = reward + rewardIncremental

    return reward


def generateMoves(board):
    moves = []
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            move = (r, c)
            if legalMove(board, move):
                moves.append(move)
    return moves


def getBestMove(board, ID, X_IN_A_LINE):
    maxReward = 0
    maxRewardPoint = 0, 0

    BOARD_SIZE = board.shape[0]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if legalMove(board, (x, y)):
                score = rewardAtPoint(ID, board, X_IN_A_LINE, (x, y))
                if score > maxReward:
                    maxReward = score
                    maxRewardPoint = x, y
    return maxRewardPoint


def minmax_decision(board):
    return 0, 0


def minimaxDecision(state):
    return state


def maxValue(state):
    return v


def minValue(state):
    return v


class Player(GomokuAgent):
    def move(self, board):
        return getBestMove(board, self.ID, self.X_IN_A_LINE)
