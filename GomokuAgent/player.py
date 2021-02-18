import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        rankedMove = 0
        move = (0, 0)

        # - For every location in the board (x coordinate and y coordinate)
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):

                # - Generates a tuple of the possible move
                moveLoc = (x, y)

                # - Checks if the move is legal on the current board
                if legalMove(board, moveLoc):

                    ''' Copies the board and sets the copy board move location to the player's id
                    (Marks the player's move as the current location on the copy board) '''
                    copyBoard = copy.deepcopy(board)
                    copyBoard[moveLoc] = self.ID

                    # - If the player has a winning move play that winning move
                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE):
                        return moveLoc



                    ''' - If the other player has a winning move block that move, we do x in a line -2 first to
                    check if they have a checkmate type move (Imagine that a player needs to get 5 in a row if
                    they have 3 in a row with both sides open they can place on one either side to get the win)'''
                    copyBoard[moveLoc] = self.ID * -1



                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE):
                        rankedMove = 4
                        move = (x, y)

                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE - 1) and rankedMove < 2:
                        rankedMove = 2
                        move = (x, y)

                    if winningTest(self.ID, copyBoard, self.X_IN_A_LINE - 2) and rankedMove < 1:
                        rankedMove = 1
                        move = (x, y)

        ''' - If no optimal move just take a random move '''
        if rankedMove > 0:
            return move

        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
