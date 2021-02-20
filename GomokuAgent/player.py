import numpy as np
import copy

from misc import legalMove, winningTest, diagTest, rowTest
from gomokuAgent import GomokuAgent


#   @return:
#   int giving number of empty spaces at ends of line for diagonals
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
                return emptyEnds
    return -1


#   @return:
#   int giving number of empty spaces at ends of line for rows
def endTestRow(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]

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
                return emptyEnds
    return -1


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

                    # - If the enemy has a winning move prioritise blocking that winning move
                    if winningTest(self.ID * -1, copyBoard, self.X_IN_A_LINE):
                        rankedMove = 2
                        move = (x, y)

                    ''' If the enemy can get 3 in a row/diagonal angle we want to block them from getting 4 if there
                    are two empty spaces '''
                    if diagTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) and rankedMove < 1 and \
                            endTestDiag(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rankedMove = 1
                        move = (x, y)

                    if rowTest(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) and rankedMove < 1 and \
                            endTestRow(self.ID * -1, copyBoard, self.X_IN_A_LINE - 1) > 1:
                        rankedMove = 1
                        move = (x, y)

        # Takes the best action that the AI found
        if rankedMove > 0:
            return move

        ''' - If no optimal move just take a random move '''
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                return moveLoc
