import numpy as np
from gomoku import BOARD_SIZE
from misc import winningTest, legalMove

import gomoku as g


def main():
    playerID = 1
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    X_IN_A_LINE = 5
    board[(0, 0)] = -1
    board[(1, 1)] = 1
    board[(2, 2)] = 1
    board[(3, 3)] = 1
    board[(4, 4)] = 1
    #board[(5, 5)] = -1
    print(endTestDiag(playerID, board, 4))


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


main()