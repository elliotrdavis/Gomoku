import numpy as np

from misc import legalMove, winningTest
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                moveLoc = (x, y)
                if legalMove(board, moveLoc):
                    copyBoard = board
                    copyBoard[x, y] = self.ID
                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE):
                        return moveLoc

        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
