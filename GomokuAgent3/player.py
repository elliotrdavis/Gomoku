import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent

def minimaxDecision(state):
    return state

def maxValue(state):
    if winningTest(ID, board, X_IN_A_LINE):
        move = bestMove(ID, board, X_IN_A_LINE)
        return move
    v = -np.inf
    return v

def minValue(state):
    if winningTest(ID, board, X_IN_A_LINE):
        move = bestMove(ID, board, X_IN_A_LINE)
        return move
    v = np.inf
    #for a, s in SUCCESSORS(state) do v<-min(v, max-value)
    return v

class Player(GomokuAgent):
    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
