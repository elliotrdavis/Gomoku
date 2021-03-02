import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
