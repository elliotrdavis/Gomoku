import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent
import gomoku

MAX = 1000000000000000
BLOCK_FIVE = 100000000
FOUR = 100000
BLOCK_FOUR = 30000
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

    # - If the player has a winning move play that winning move
    if winningTest(ID, copyBoard, X_IN_A_LINE):
        return MAX

    ''' - If the other player has a winning move block that move, we do x in a line -2 first to
    check if they have a checkmate type move (Imagine that a player needs to get 5 in a row if
    they have 3 in a row with both sides open they can place on one either side to get the win)'''
    copyBoard[point] = ID * -1

    # - If the enemy has a winning move prioritise blocking that winning move
    if winningTest(ID * -1, copyBoard, X_IN_A_LINE):
        return BLOCK_FIVE

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

    return bestReward, bestRewardPoint


def generateMoves(board):
    moves = []
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            move = (r, c)
            if legalMove(board, move):
                moves.add(move)
    return moves



# Assigns a board a score with respect to a player, given by playerID. Score is dependent on the rows
# and lines a player has on the board.
def evaluateBoard(playerID, board, X_IN_A_LINE):
    score = 0
    copyBoard = copy.deepcopy(board)
    score += scoreRows(playerID, copyBoard, X_IN_A_LINE) + scoreDiags(playerID, copyBoard, X_IN_A_LINE)

    rotatedBoard = np.rot90(copyBoard)
    score += scoreRows(playerID, rotatedBoard, X_IN_A_LINE) + scoreDiags(playerID, rotatedBoard, X_IN_A_LINE)

    return score


def scoreRows(playerID, board, X_IN_A_LINE):
    boardScore = 0
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
            rowLength = 0
            blocked = False
            for i in range(X_IN_A_LINE):
                if board[r + i, c] == playerID:
                    rowLength += 1
                elif board[r + i, c] == -playerID:
                    blocked = True
                    break
            if not blocked:
                boardScore += lineScore(rowLength, X_IN_A_LINE)
    return boardScore


def scoreDiags(playerID, board, X_IN_A_LINE):
    boardScore = 0
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
            rowLength = 0
            blocked = False
            for i in range(X_IN_A_LINE):
                if board[r + i, c + i] == playerID:
                    rowLength += 1
                elif board[r + i, c + i] == -playerID:
                    blocked = True
                    break
            if not blocked:
                boardScore += lineScore(rowLength, X_IN_A_LINE)
    return boardScore


def lineScore(lineLength, X_IN_A_LINE):
    if lineLength == X_IN_A_LINE:
        return 2 ** (lineLength ** 2)
    return 2 ** lineLength



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
        score, move = minimax(self.ID, board, self.X_IN_A_LINE, 2, -MAX, MAX, True)
        print(move)
        return move