import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent

MAX = 1000000000000000
BLOCK_FIVE = 100000000
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


def rewardAtPoint(ID, board, X_IN_A_LINE, point):
    """ - Sets the base value of the reward to the max distance subtract the distance between the move
        and center """
    maxDistance = distance((0, 0), (board.shape[0], board.shape[0]))
    center = centroid(ID, board)
    reward = maxDistance - distance(point, center)

    copyBoard = copy.deepcopy(board)
    copyBoard[point] = ID

    # - If the player has a winning move play that winning move
    if winningTest(ID, copyBoard, X_IN_A_LINE):
        reward = reward + MAX

    ''' - If the other player has a winning move block that move, we do x in a line -2 first to
    check if they have a checkmate type move (Imagine that a player needs to get 5 in a row if
    they have 3 in a row with both sides open they can place on one either side to get the win)'''
    copyBoard[point] = ID * -1

    # - If the enemy has a winning move prioritise blocking that winning move
    if winningTest(ID * -1, copyBoard, X_IN_A_LINE):
        reward = reward + BLOCK_FIVE

    # - If the player can get 4 in a row with 2 empty spaces
    copyBoard[point] = ID
    if diagTest(ID, copyBoard, X_IN_A_LINE - 1) and \
            endTestDiag(ID, copyBoard, X_IN_A_LINE - 1) > 1:
        reward = reward + FOUR

    if rowTest(ID, copyBoard, X_IN_A_LINE - 1) and \
            endTestRow(ID, copyBoard, X_IN_A_LINE - 1) > 1:
        reward = reward + FOUR

    ''' If the enemy can get 3 in a row/diagonal angle we want to block them from getting 4 if there
    are two empty spaces '''
    copyBoard[point] = ID * -1
    if diagTest(ID * -1, copyBoard, X_IN_A_LINE - 1) and \
            endTestDiag(ID * -1, copyBoard, X_IN_A_LINE - 1) > 1:
        reward = reward + BLOCK_FOUR

    if rowTest(ID * -1, copyBoard, X_IN_A_LINE - 1) and \
            endTestRow(ID * -1, copyBoard, X_IN_A_LINE - 1) > 1:
        reward = reward + BLOCK_FOUR

    # - If the player can get 3 in a row with 2 empty spaces
    copyBoard[point] = ID
    if diagTest(ID, copyBoard, X_IN_A_LINE - 2) and \
            endTestDiag(ID, copyBoard, X_IN_A_LINE - 2) > 1:
        reward = reward + THREE

    if rowTest(ID, copyBoard, X_IN_A_LINE - 2) and \
            endTestRow(ID, copyBoard, X_IN_A_LINE - 2) > 1:
        reward = reward + THREE

    ''' If the enemy can get 2 in a row/diagonal angle we want to block them from getting 3 if there
        are two empty spaces '''
    copyBoard[point] = ID * -1
    if diagTest(ID * -1, copyBoard, X_IN_A_LINE - 2) and \
            endTestDiag(ID * -1, copyBoard, X_IN_A_LINE - 2) > 1:
        reward = reward + BLOCK_FOUR

    if rowTest(ID * -1, copyBoard, X_IN_A_LINE - 2) and \
            endTestRow(ID * -1, copyBoard, X_IN_A_LINE - 2) > 1:
        reward = reward + BLOCK_THREE

    # - If the player can get 2 in a row with 2 empty spaces
    copyBoard[point] = ID
    if diagTest(ID, copyBoard, X_IN_A_LINE - 3) and \
            endTestDiag(ID, copyBoard, X_IN_A_LINE - 3) > 1:
        reward = reward + TWO

    if rowTest(ID, copyBoard, X_IN_A_LINE - 3) and \
            endTestRow(ID, copyBoard, X_IN_A_LINE - 3) > 1:
        reward = reward + TWO

    ''' If the enemy can get 1 in a row/diagonal angle we want to block them from getting 2 if there
        are two empty spaces '''
    copyBoard[point] = ID * -1
    if diagTest(ID * -1, copyBoard, X_IN_A_LINE - 3) and \
            endTestDiag(ID * -1, copyBoard, X_IN_A_LINE - 3) > 1:
        reward = reward + BLOCK_TWO

    if rowTest(ID * -1, copyBoard, X_IN_A_LINE - 3) and \
            endTestRow(ID * -1, copyBoard, X_IN_A_LINE - 3) > 1:
        reward = reward + BLOCK_TWO

    return reward


def bestMoveAndReward(ID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    rewards = np.zeros((BOARD_SIZE, BOARD_SIZE))

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            # - Generates a tuple of the possible move
            moveLoc = (x, y)

            # - Checks if the move is legal on the current board
            if legalMove(board, moveLoc):
                rewards[moveLoc] = rewardAtPoint(ID, board, X_IN_A_LINE, moveLoc)

    bestReward = 0
    bestRewardPoint = 0, 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if rewards[(i, j)] > bestReward:
                bestReward = rewards[(i, j)]
                bestRewardPoint = i, j

    return bestReward, bestRewardPoint


def minimax(ID, board, X_IN_A_LINE, depth, alpha, beta, maxPlayer):
    BOARD_SIZE = board.shape[0]

    # Takes the best action that the AI found
    # - Checks if depth is equal to 0 or the game is over
    if depth == 0 or winningTest(ID, board, X_IN_A_LINE) or winningTest(ID * -1, board, X_IN_A_LINE):
        if maxPlayer:
            return bestMoveAndReward(ID, board, X_IN_A_LINE)
        else:
            reward, move = bestMoveAndReward(ID, board, X_IN_A_LINE)
            return -reward, move

    if maxPlayer:
        maxEval = -100000000000000000000000000000
        maxEvalPoint = (0, 0)

        # - For every location in the board (x coordinate and y coordinate)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # - Generates a tuple of the possible move
                moveLoc = (x, y)

                # - Checks if the move is legal on the current board
                if legalMove(board, moveLoc):
                    copyBoard = copy.deepcopy(board)
                    value = rewardAtPoint(ID, board, X_IN_A_LINE, moveLoc)
                    copyBoard[moveLoc] = ID

                    eval, move = minimax(ID * -1, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta, False)
                    eval = eval + value
                    if eval > maxEval:
                        maxEval = eval
                        maxEvalPoint = moveLoc
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
        return maxEval, maxEvalPoint

    else:
        minEval = 100000000000000000000000000000000
        minEvalPoint = (0, 0)

        # - For every location in the board (x coordinate and y coordinate)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # - Generates a tuple of the possible move
                moveLoc = (x, y)

                # - Checks if the move is legal on the current board
                if legalMove(board, moveLoc):
                    copyBoard = copy.deepcopy(board)
                    value = rewardAtPoint(ID, board, X_IN_A_LINE, moveLoc)
                    copyBoard[moveLoc] = ID

                    eval, move = minimax(ID * -1, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta, True)
                    eval = eval - value
                    if eval < minEval:
                        minEval = eval
                        minEvalPoint = moveLoc
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return minEval, minEvalPoint


class Player(GomokuAgent):
    def move(self, board):
        score, move = minimax(self.ID, board, self.X_IN_A_LINE, 1, -100000000000000000000000000000000,
                              100000000000000000000000000000000, True)
        return move
