import numpy as np
from gomoku import BOARD_SIZE
from misc import winningTest#, legalMove
import gomoku as g


def main():
    playerID = 1
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    X_IN_A_LINE = 5
    board[(1, 0)] = -1
    board[(1, 1)] = 1
    board[(1, 2)] = 1
    board[(1, 3)] = 1
    board[(1, 4)] = 1
    #board[(5, 5)] = -1
    print(endTestRow(playerID, board, 4))


# @return:
#   boolean: True if the board has
#   int giving number of empty spaces at ends of line, o

def endTestDiag(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):

            emptyEnds = 0
            if legalMove(board, (r - 1, c - 1)):
                if board[r - 1, c - 1] == 0:
                    emptyEnds += 1
            if legalMove(board, (r + X_IN_A_LINE, c + X_IN_A_LINE)):
                if board[r + X_IN_A_LINE, c + X_IN_A_LINE] == 0:
                    emptyEnds += 1

            flag = True
            for i in range(X_IN_A_LINE):
                if board[r + i, c + i] != playerID:
                    flag = False
                    break
            if flag:
                return True, emptyEnds
    return False, -1

def endTestRow(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    mask = np.ones(X_IN_A_LINE, dtype=int) * playerID

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):

            emptyEnds = 0
            if legalMove(board, (r, c - 1)):
                if board[r, c - 1] == 0:
                    emptyEnds += 1
            if legalMove(board, (r, c + X_IN_A_LINE)):
                if board[r, c + X_IN_A_LINE] == 0:
                    emptyEnds += 1

            flag = True
            for i in range(X_IN_A_LINE):
                if board[r, c + i] != playerID:
                    flag = False
                    break
            if flag:
                return True

    return False

def legalMove(board, moveLoc):
    BOARD_SIZE = board.shape[0]
    if moveLoc[0] < 0 or moveLoc[0] >= BOARD_SIZE or \
            moveLoc[1] < 0 or moveLoc[1] >= BOARD_SIZE:
        return False

    if board[moveLoc] == 0:
        return True
    return False


main()