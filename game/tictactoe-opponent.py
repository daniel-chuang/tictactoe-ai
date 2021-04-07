# Simple game of tictactoe on Pygame to experiment with.
## This version is the base version of tictactoe.
## There is no opponent yet, this is a 2 player game right now.

# Imports
import pygame
import time
import numpy as np
import sys
import random

# Constants
BLOCKSIZE = 200 # The pixel size of each block
HEIGHT = 3 # The height of the grid (in blocks)
WIDTH = 3 # The width of the grid (in blocks)

# Classes
class Cursor():
    """
    The "cursor" is really a hovered block. In the actual screen, this will
    be outlined with a colored border to indicate to the user that they are
    selecting that block.

    This cursor is how the user will select a block to claim for their turn.

    The position of the cursor will be controlled by the user's arrow keys.
    WASD keys will also be functional, as an alternative. The cursor will start
    at the top left corner when the game begins.

    The parameters of this class are:
    x: the x position of the cursor
    y: the y position of the cursor
    width: the width of the grid (in blocks) to limit the x by. DEFAULT = WIDTH - 1
    height: the height of the grid (in blocks) to limit the y by. DEFAULT = HEIGHT - 1

    The attributes are all the same as the parameters of class. However,
    width and height are replaced by xlim and ylim, which are both 1 smaller
    than the original width and height (since matrix indexing starts at 0).
    """
    def __init__(self, x=0, y=0, width=WIDTH, height= HEIGHT):
        self.x = x
        self.y = y
        self.xlim = width - 1
        self.ylim = height - 1

    def move(self, direction: str):
        """
        Moves the cursor in a direction.

        The direction parameter is a string.
        Left: "left"
        Right: "right"
        Up: "up"
        Down: "down"
        """
        if direction == "left":
            if self.x > 0:
                self.x -= 1
        if direction == "right":
            if self.x < self.xlim:
                self.x += 1
        if direction == "down":
            if self.y < self.ylim:
                self.y += 1
        if direction == "up":
            if self.y > 0:
                self.y -= 1

class Grid():
    """
    Creates a grid for the tictactoe game using a 2D numpy array.

    The parameters of this class are:
    width: the width of the grid (in blocks). DEFAULT = WIDTH
    height: the height of the grid (in blocks). DEFAULT = HEIGHT
    cursor: an object from the Cursor class
    """
    def __init__(self, width = WIDTH, height = HEIGHT, blocksize = BLOCKSIZE):
        self.width = width
        self.height = height
        self.blocksize = blocksize

        # In the numpy array:
        # 0 represents an empty state
        # 1 represents a space claimed by the first player
        # 2 represents a space claimed by the second player
        self.matrix = np.full([3, 3], 0, dtype = int)

    def InitiateEmptyBoard(self):
        self.matrix = np.full([3, 3], 0, dtype = int)

    def ClaimBlock(self, x: int, y: int, player: int = 1):
        if self.matrix[y, x] == 0: # if the block is empty, then it can be claimed.
            self.matrix[y, x] = player
            return(True)
        return(False)

    def CheckWin(self):
        # Check for a win
        matrixList = [self.matrix, np.transpose(self.matrix)] # self.matrix for rows, np.transpose(self.matrix) for columns
        matrixList.append([np.diag(matrix, k=0) for matrix in [self.matrix, np.rot90(self.matrix)]]) # appends diagonals
        for matrix in matrixList: # for rows and columns and diagonals(transpose for columns)
            for row in matrix: # for row checking
                for n in [1,2]: # for player 1 and player 2
                    booleRow = row[row == n]
                    if booleRow.shape[0] == 3: # if the row is full, then a player wins
                        self.matrix = np.full([3, 3], n, dtype = int)
                        print(f"Player {n} Wins")
                        return(True)
        # Check for a tie
        if np.count_nonzero(self.matrix) == self.width * self.height: # checks if the matrix has a full grid
            print(f"The board is full, so this game is a tie!")
            return(True)

class Opponent():
    """
    Newell and Simon's 1972 tic-tac-toe program algorithm:
    https://en.wikipedia.org/wiki/Tic-tac-toe

    Win: If the player has two in a row, they can place a third to get three in a row.
    Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
    Fork: Create an opportunity where the player has two ways to win (two non-blocked lines of 2).
    Blocking an opponent's fork: If there is only one possible fork for the opponent, the player should block it. Otherwise, the player should block all forks in any way that simultaneously allows them to create two in a row. Otherwise, the player should create a two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork. For example, if "X" has two opposite corners and "O" has the center, "O" must not play a corner move in order to win. (Playing a corner move in this scenario creates a fork for "X" to win.)
    Center: A player marks the center. (If it is the first move of the game, playing a corner move gives the second player more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
    Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
    Empty corner: The player plays in a corner square.
    Empty side: The player plays in a middle square on any of the 4 sides.
    """
    def __init__(self, Cursor, Grid):
        self.Grid = Grid
        self.Cursor = Cursor

    def Algorithm(self):
        """
        Performs the algorithm in the docstring of the "Opponent" class. Returns the position of a move in x, y.
        """
        funcs = [self.CheckWin(),
                 self.CheckBlock(),
                 self.CheckFork(),
                 self.CheckBlockFork(),
                 self.CheckCenter(),
                 self.CheckOppositeCorners(),
                 self.CheckEmptyCorner(),
                 self.CheckEmptyCorner()
                ]
        """
        self.CheckWin()
        self.CheckBlock()
        self.CheckFork()
        self.CheckBlockFork()
        self.CheckCenter()
        self.CheckOppositeCorners()
        self.CheckEmptyCorner()
        self.CheckEmptySide()
        """
        for func in funcs:
            if func != None:
                return(func)

    def CheckWin(self):
        matrixList = [self.Grid.matrix, np.transpose(self.Grid.matrix)] # self.matrix for rows, np.transpose(self.matrix) for columns
        matrixList.append([np.diag(matrix, k=0) for matrix in [self.Grid.matrix, np.rot90(self.Grid.matrix)]]) # appends diagonals
        for matrix in matrixList: # for rows and columns and diagonals(transpose for columns)
            for row in matrix: # for row checking
                booleRow = row[row != 0]
                if booleRow[booleRow == 1].shape[0] != 0:
                    continue
                elif booleRow.shape[0] == 2:
                    return("Check Win")
        return(None)

    def CheckBlock(self):
        matrixList = [self.Grid.matrix, np.transpose(self.Grid.matrix)] # self.matrix for rows, np.transpose(self.matrix) for columns
        matrixList.append([np.diag(matrix, k=0) for matrix in [self.Grid.matrix, np.rot90(self.Grid.matrix)]]) # appends diagonals
        for matrix in matrixList: # for rows and columns and diagonals(transpose for columns)
            for row in matrix: # for row checking
                booleRow = row[row != 0]
                if booleRow[booleRow == 2].shape[0] != 0:
                    continue
                elif booleRow.shape[0] == 2:
                    return("Check Block")
        return(None)

    def CheckFork(self):
        # Makes an x and y list of all open blocks
        openBlocksX = []
        openBlocksY = []
        for x in range(0,3):
            for y in range(0,3):
                if self.Grid.matrix[y, x] == 0:
                    openBlocksX.append(x)
                    openBlocksY.append(y)

        # Checks if playing in an open spot will make a fork
        for x in openBlocksX:
            for y in openBlocksY:
                winCount = 0
                tempMatrix = np.copy(self.Grid.matrix)
                tempMatrix[y, x] = 2
                matrixList = [tempMatrix, np.transpose(tempMatrix)] # self.tempMatrix for rows, np.transpose(self.tempMatrix) for columns
                matrixList.append([np.diag(tempMatrix, k=0) for tempMatrix in [tempMatrix, np.rot90(tempMatrix)]]) # appends diagonals
                for matrix in matrixList: # for rows and columns and diagonals(transpose for columns)
                    for row in matrix: # for row checking
                        booleRow = row[row != 0]
                        if booleRow[booleRow == 1].shape[0] != 0:
                            continue
                        elif booleRow.shape[0] == 2:
                            winCount += 1
                if winCount >= 2:
                    return("Check Fork")
        return(None)

    def CheckBlockFork(self):
        # Makes an x and y list of all open blocks
        openBlocksX = []
        openBlocksY = []
        for x in range(0,3):
            for y in range(0,3):
                if self.Grid.matrix[y, x] == 0:
                    openBlocksX.append(x)
                    openBlocksY.append(y)

        # Checks if playing in an open spot will make a fork
        for x in openBlocksX:
            for y in openBlocksY:
                winCount = 0
                tempMatrix = np.copy(self.Grid.matrix)
                tempMatrix[y, x] = 1
                matrixList = [tempMatrix, np.transpose(tempMatrix)] # self.tempMatrix for rows, np.transpose(self.tempMatrix) for columns
                matrixList.append([np.diag(tempMatrix, k=0) for tempMatrix in [tempMatrix, np.rot90(tempMatrix)]]) # appends diagonals
                for matrix in matrixList: # for rows and columns and diagonals(transpose for columns)
                    for row in matrix: # for row checking
                        booleRow = row[row != 0]
                        if booleRow[booleRow == 2].shape[0] != 0:
                            continue
                        elif booleRow.shape[0] == 2:
                            winCount += 1
                if winCount >= 2:
                    return("Check Block Fork")
        return(None)

    def CheckCenter(self):
        if self.Grid.matrix[1,1] == 0:
            return("Check Center")
        return(None)

    def CheckOppositeCorners(self):
        for x in [0, 2]:
            for y in [0, 2]:
                if self.Grid.matrix[y, x] == 1 and self.Grid.matrix[abs(y-2), abs(x-2)] == 0:
                    return("Check Opposite Corners")
        return(None)

    def CheckEmptyCorner(self):
        for x in [0, 2]:
            for y in [0, 2]:
                if self.Grid.matrix[y, x] == 0:
                    return("Check Empty Corners")
        return(None)

    def CheckEmptySide(self):
        if self.Grid.matrix[0,1] == 0:
            return("Check Empty Side")
        elif self.Grid.matrix[1,0] == 0:
            return("Check Empty Side")
        elif self.Grid.matrix[0,2] == 0:
            return("Check Empty Side")
        elif self.Grid.matrix[2,0] == 0:
            return("Check Empty Side")

def main():
    # Initialize pygame
    pygame.init()

    # Initialize grid, cursor
    grid = Grid()
    cursor = Cursor()

    # Initialize opponent
    opponent = Opponent(cursor, grid)

    # Initialize a screen
    screen = pygame.display.set_mode((BLOCKSIZE * WIDTH, BLOCKSIZE * HEIGHT))
    clock = pygame.time.Clock()

    # Initiate active player
    current_player = random.randint(1,2)
    if current_player == 2:
        print(opponent.Algorithm())

    # Main loop
    ## Pygame events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cursor.move("right")
                if event.key == pygame.K_LEFT:
                    cursor.move("left")
                if event.key == pygame.K_UP:
                    cursor.move("up")
                if event.key == pygame.K_DOWN:
                    cursor.move("down")
                if event.key == pygame.K_SPACE:
                    if grid.ClaimBlock(cursor.x, cursor.y, current_player):
                        current_player = {1: 2, 2: 1}[current_player]
                        if current_player == 2:
                            # Opponent Move
                            print(opponent.Algorithm())

        # Fill Pygame screen
        screen.fill((0,0,0))

        # Draw blocks
        for h in range(len(grid.matrix)):
            for w in range(len(grid.matrix[0])):
                if grid.matrix[h][w] == 1: # draw red blocks for player 1
                    pygame.draw.rect(screen, (255, 0, 0),
                                        (w * BLOCKSIZE + 5, h * BLOCKSIZE + 5, BLOCKSIZE - 5, BLOCKSIZE - 5))
                if grid.matrix[h][w] == 2: # draw blue blocks for player 2
                    pygame.draw.rect(screen, (0, 0, 255),
                                        (w * BLOCKSIZE + 5, h * BLOCKSIZE + 5, BLOCKSIZE - 5, BLOCKSIZE - 5))

        # Draw cursor highlight
        if current_player == 1:
            pygame.draw.rect(screen, (255, 0, 0), (cursor.x * BLOCKSIZE, cursor.y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 7)
        else:
            pygame.draw.rect(screen, (0, 0, 255), (cursor.x * BLOCKSIZE, cursor.y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 7)

        # Update Screen
        pygame.display.update()

        # Check for winner
        if grid.CheckWin():
            time.sleep(1)
            pygame.quit()
            sys.exit()
main()