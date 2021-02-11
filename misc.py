import sys
import numpy as np

def legalMove(board, moveLoc):
    BOARD_SIZE = board.shape[0]
    if moveLoc[0] < 0 or moveLoc[0] >= BOARD_SIZE or \
       moveLoc[1] < 0 or moveLoc[1] >= BOARD_SIZE: 
        return False

    if board[moveLoc] == 0:
        return True
    return False

def rowTest(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    mask = np.ones(X_IN_A_LINE, dtype=int)*playerID

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE-X_IN_A_LINE+1):
            flag = True
            for i in range(X_IN_A_LINE):
                if board[r,c+i] != playerID:
                    flag = False
                    break
            if flag:
                return True

    return False        

def diagTest(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
            flag = True
            for i in range(X_IN_A_LINE):
                if board[r+i,c+i] != playerID:
                    flag = False
                    break
            if flag:
                return True
    return False

def winningTest(playerID, board, X_IN_A_LINE):  
    if rowTest(playerID, board, X_IN_A_LINE) or diagTest(playerID, board, X_IN_A_LINE):
        return True

    boardPrime = np.rot90(board)
    if rowTest(playerID, boardPrime, X_IN_A_LINE) or diagTest(playerID, boardPrime, X_IN_A_LINE):
        return True
    
    return False
