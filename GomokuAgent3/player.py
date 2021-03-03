import numpy as np
import copy

from misc import legalMove, diagTest, rowTest, winningTest
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
        for c in range(BOARD_SIZE - 1):
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
        return 10 ** 10
    elif lineLength == X_IN_A_LINE - 1:
        return 10 ** 4
    elif lineLength == X_IN_A_LINE - 2:
        return 10 ** 3
    elif lineLength == X_IN_A_LINE - 3:
        return 10 ** 2
    return 0


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

        rewardIncremental = 2 * (rewardIncremental ** 2)

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
    return maxReward, maxRewardPoint


def minimaxDecision(ID, board, X_IN_A_LINE, d, cutoff_test, eval_fn):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    #player = game.to_move(state) - ID
    #state = board
    # Functions used by alpha_beta


    def max_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return eval_fn(board)
        v = -np.inf
        for a in generateMoves(board):
            copyBoard = copy.deepcopy(board)
            copyBoard[a] = ID
            v = max(v, min_value(copyBoard, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return eval_fn(board)
        v = np.inf
        #print(board)
        for a in generateMoves(board):
            copyBoard = copy.deepcopy(board)
            copyBoard[a] = ID
            v = min(v, max_value(copyBoard, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def terminal_test(ID, board, X_IN_A_LINE):
        #print(board)
        if winningTest(ID, board, X_IN_A_LINE) or winningTest(ID * -1, board, X_IN_A_LINE):
            return True
        else:
            return False


    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    #print(board)
    cutoff_test = (cutoff_test or (lambda board, depth: depth > d or terminal_test(ID, board, X_IN_A_LINE)))
    eval_fn = eval_fn or (lambda board: evaluateBoard(ID, board, X_IN_A_LINE)) # Returns the value of this final state to the player
    #evaluateBoard(playerID, board, X_IN_A_LINE)
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in generateMoves(board):
        copyBoard = copy.deepcopy(board)
        copyBoard[a] = ID
        v = min_value(copyBoard, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

    #
    # def maxValue(ID, board, X_IN_A_LINE, depth):
    #     if winningTest(ID, board, X_IN_A_LINE) or winningTest(ID * -1, board, X_IN_A_LINE):
    #         return 0, (0, 0)
    #
    #     if depth == 0:
    #         return getBestMove(board, ID, X_IN_A_LINE)
    #
    #     v = -np.inf
    #     maxMove = 0, 0
    #     for x in generateMoves(board):
    #         copyBoard = copy.deepcopy(board)
    #         copyBoard[x] = ID
    #         score, move = minValue(ID, copyBoard, X_IN_A_LINE, depth - 1)
    #         score2 = rewardAtPoint(ID, board, X_IN_A_LINE, x)
    #         if score + score2 > v:
    #             v = max(v, score + score2)
    #             maxMove = x
    #     return v, maxMove
    #
    # def minValue(ID, board, X_IN_A_LINE, depth):
    #     if winningTest(ID, board, X_IN_A_LINE) or winningTest(ID * -1, board, X_IN_A_LINE):
    #         return getBestMove(board, ID, X_IN_A_LINE)
    #
    #     if depth == 0:
    #         return getBestMove(board, ID, X_IN_A_LINE)
    #
    #     v = np.inf
    #     minMove = 0, 0
    #     for x in generateMoves(board):
    #         copyBoard = copy.deepcopy(board)
    #         copyBoard[x] = ID
    #         score, move = maxValue(ID, copyBoard, X_IN_A_LINE, depth - 1)
    #         score2 = rewardAtPoint(ID, board, X_IN_A_LINE, x)
    #         if score - score2 < v:
    #             v = min(v, score - score2)
    #             minMove = x
    #     return v, minMove
    #
    # return maxValue(ID, board, X_IN_A_LINE, depth)


class Player(GomokuAgent):
    def move(self, board):
        move = minimaxDecision(self.ID, board, self.X_IN_A_LINE, 1, None, None)
        return move
