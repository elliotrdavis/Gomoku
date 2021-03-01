import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent


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
    """ - Sets the base value of the reward to the max distance subtract the distance between the move
        and center """
    maxDistance = distance((0, 0), (board.shape[0], board.shape[0]))
    center = centroid(ID, board)
    reward = maxDistance - distance(point, center)

    copyBoard = copy.deepcopy(board)
    copyBoard[point] = ID

    # - This is a fixed amount each amount doubles each possible move
    incrementalReward = 1000

    for x in range(2, X_IN_A_LINE + 1):
        copyBoard[point] = ID * -1
        copyBoardPrime = np.rot90(copyBoard)

        # - If the player can get 4 in a row with 2 empty spaces
        if diagTest(ID * - 1, copyBoard, x) and \
                endTestDiag(ID * -1, copyBoard, x) > 1:
            reward = reward + incrementalReward

        if diagTest(ID * - 1, copyBoardPrime, x) and \
                endTestDiag(ID * -1, copyBoardPrime, x) > 1:
            reward = reward + incrementalReward

        # - If the player can get 4 in a row with 2 empty spaces
        if rowTest(ID * - 1, copyBoard, x) and \
                endTestRow(ID * -1, copyBoard, x) > 1:
            reward = reward + incrementalReward

        if rowTest(ID * - 1, copyBoardPrime, x) and \
                endTestRow(ID * -1, copyBoardPrime, x) > 1:
            reward = reward + incrementalReward

        incrementalReward = incrementalReward * 5

        copyBoard[point] = ID
        copyBoardPrime = np.rot90(copyBoard)

        # - If the player can get 4 in a row with 2 empty spaces
        if diagTest(ID, copyBoard, x) and \
                endTestDiag(ID, copyBoard, x) > 1:
            reward = reward + incrementalReward

        if diagTest(ID, copyBoardPrime, x) and \
                endTestDiag(ID, copyBoardPrime, x) > 1:
            reward = reward + incrementalReward

        incrementalReward = incrementalReward * 5

    return reward


def bestMoveAndReward(ID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    rewards = np.zeros((BOARD_SIZE, BOARD_SIZE))
    bestReward = 0
    bestRewardPoint = 0, 0

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            # - Generates a tuple of the possible move
            moveLoc = (x, y)

            # - Checks if the move is legal on the current board
            if legalMove(board, moveLoc):
                rewards[moveLoc] = rewardAtPoint(ID, board, X_IN_A_LINE, moveLoc)
                if rewards[moveLoc] > bestReward:
                    bestReward = rewards[moveLoc]
                    bestRewardPoint = moveLoc

    print(np.round(rewards))
    return bestReward, bestRewardPoint


def minimax(ID, board, X_IN_A_LINE, depth, alpha, beta, maxPlayer):
    # Takes the best action that the AI found
    # - Checks if depth is equal to 0 or the game is over
    if depth == 0 or winningTest(ID, board, X_IN_A_LINE) or winningTest(ID * -1, board, X_IN_A_LINE):
        reward, move = bestMoveAndReward(ID, board, X_IN_A_LINE)
        if (maxPlayer):
            return reward, move
        else:
            return (reward * -1), move

    BOARD_SIZE = board.shape[0]

    if maxPlayer:
        maxEval = -(MAX * 7)
        maxEvalPoint = 0, 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                moveLoc = (x, y)

                if legalMove(board, moveLoc):
                    value = rewardAtPoint(ID, board, X_IN_A_LINE, (x, y))
                    copyBoard = copy.deepcopy(board)
                    copyBoard[moveLoc] = ID

                    evaluation, move = minimax(ID * - 1, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta, False)
                    evaluation = value + evaluation
                    if evaluation > maxEval:
                        maxEval = evaluation
                        maxEvalPoint = moveLoc
                        alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break

        return maxEval, maxEvalPoint

    else:
        minEval = MAX * 7
        minEvalPoint = 0, 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                moveLoc = (x, y)

                if legalMove(board, moveLoc):
                    value = rewardAtPoint(ID, board, X_IN_A_LINE, moveLoc)
                    copyBoard = copy.deepcopy(board)
                    copyBoard[moveLoc] = ID

                    evaluation, move = minimax(ID * - 1, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta, True)
                    evaluation = (value * -1) + evaluation
                    if evaluation < minEval:
                        minEval = evaluation
                        minEvalPoint = moveLoc
                        beta = min(beta, minEval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break

        return minEval, minEvalPoint


class Player(GomokuAgent):
    def move(self, board):
        score, move = minimax(self.ID, board, self.X_IN_A_LINE, 0, 0, 0, True)
        return move
