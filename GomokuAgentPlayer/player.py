import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        while True:
            print("Enter X then Y input")
            print("X:")
            xInput = int(input())
            print("Y:")
            yInput = int(input())

            moveLoc = (xInput, yInput)
            if legalMove(board, moveLoc):
                return moveLoc

