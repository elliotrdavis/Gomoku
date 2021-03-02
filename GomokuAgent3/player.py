import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

def minimaxDecision(state):
    return state

def maxValue(state):
    return v

def minValue(state):
    retrun v

class Player(GomokuAgent):
    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
