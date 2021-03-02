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


def generateMoves(board):
    moves = []
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            move = (r, c)
            if legalMove(board, move):
                moves.append(move)
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


def findWinningMove(moves, ID, board, X_IN_A_LINE):
    copyBoard = copy.deepcopy(board)
    for move in moves:
        copyBoard[move] = ID
        if move == (3, 3):
            print("33")
        if winningTest(ID, copyBoard, X_IN_A_LINE):
            return move
        copyBoard[move] = 0

    return None


def calculateMove(ID, board, X_IN_A_LINE, depth):
    moves = generateMoves(board)

    # return winning move if can win instantly
    winningMove = findWinningMove(moves, ID, board, X_IN_A_LINE)
    if winningMove is not None:
        return winningMove

    bestScore, bestMoveR, bestMoveC = minimax(True, moves, ID, board, X_IN_A_LINE, depth, alpha=-1,
                                              beta=lineScore(X_IN_A_LINE, X_IN_A_LINE))
    if bestMoveR is None or bestMoveC is None:
        move = None
    else:
        move = (bestMoveR, bestMoveC)

    return move


'''
@return - int score, int bestMoveX, int bestMoveY
'''


def minimax(maxPlayer, moves, ID, board, X_IN_A_LINE, depth, alpha, beta):
    if depth == 0:
        evaluation = evaluateBoard(ID, board, X_IN_A_LINE), None, None
        return evaluation

    # moves = generateMoves(board)
    if len(moves) == 0:
        return evaluateBoard(-ID, board, X_IN_A_LINE), None, None

    bestMoveR = None
    bestMoveC = None

    if maxPlayer:
        bestScore = -1
        copyMoves = copy.deepcopy(moves)
        for move in copyMoves:
            # Create a copy of the board in its current state
            copyBoard = copy.deepcopy(board)

            # Perform the move (we have already established that this move is a
            # legal move in generateMoves
            copyBoard[move] = -ID

            copyMoves.remove(move)

            maxPlayer = False
            # Call minimax for next depth
            tempScore, tempMoveR, tempMoveC = minimax(maxPlayer, copyMoves, -ID, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta)

            if tempScore > bestScore:
                bestScore = tempScore
                bestMoveR = move[0]
                bestMoveC = move[1]

        if bestScore < -1:
            print("AAAAAAAAH")




    else:
        bestScore = 2 * lineScore(X_IN_A_LINE, X_IN_A_LINE)
        bestMoveR = moves[0][0]
        bestMoveC = moves[0][1]

        copyMoves = copy.deepcopy(moves)
        for move in moves:
            copyBoard = copy.deepcopy(board)

            copyBoard[move] = ID

            copyMoves.remove(move)

            maxPlayer = True

            tempScore, tempMoveR, tempMoveC = minimax(maxPlayer, copyMoves, ID, copyBoard, X_IN_A_LINE, depth - 1, alpha, beta)

            if tempScore < bestScore:
                bestScore = tempScore
                bestMoveR = move[0]
                bestMoveC = move[1]

    #print(bestScore, bestMoveR, bestMoveC, depth)
    return bestScore, bestMoveR, bestMoveC


class Player(GomokuAgent):
    def move(self, board):
        move = calculateMove(self.ID, board, self.X_IN_A_LINE, 3)
        # print(move)
        return move
