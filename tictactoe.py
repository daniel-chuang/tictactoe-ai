"""
Tic Tac Toe Player
"""

import math
import numpy as np
import collections
import copy
import time

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    Note: the first player in this game is always X.
    """
    # Initializes the collections Counter class, counting how many X's and O's there are on the board
    count = collections.Counter()
    for row in board:
        for element in row:
            count[element] += 1

    # If the amount of X's is equal to the amount of O's, then it must be X's turn.
    if count["X"] == count["O"]:
        return "X"
    # Elsewise, it must be O's turn
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initializes a frontier set
    actions_frontier = list()

    # Loops through every single spot on the board and add the coordinates to the frontier if it is empty
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions_frontier.append((i, j))

    return actions_frontier

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Raises an error if the action on the board is impossible
    try:
        if board[action[0]][action[1]] != None:
            raise ValueError("The action provided for the board was not possible.")
    except TypeError:
        print("TypeError:", board, action)

    # Uses copy.deepcopy so that the original board is not modified
    new_board = copy.deepcopy(board)

    # Returns the boardstate after the action has occurred
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Rotated board
    board_rotated = list()
    for j in range(3):
        board_rotated.append([board[0][j], board[1][j], board[2][j]])

    # Conversion to numpy array
    board = np.array(board)
    board_rotated = np.array(board_rotated)

    # Different boards for horizontal, vertical, positive slope diagonal, negative slope diagonal
    for board_iter in [board, board_rotated, np.diagonal(board), np.diagonal(np.fliplr(board))]:
        if board_iter.shape == (3,3):
            for line in board_iter: # Checks each "line" in a board
                for block in ["X", "O"]: # Checks for both players
                    if np.count_nonzero(line == block) == 3: # If that "line" is occupied by three of the same things, return the winner
                        return block
        else:
            for block in ["X", "O"]: # Checks for both players
                if np.count_nonzero(board_iter == block) == 3: # If that "line" is occupied by three of the same things, return the winner
                    return block

    # Returns None if there is no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checks if anyone has won
    if winner(board) != None:
        return True

    # Checks if there is a tie using np.count_nonzero. If there are 9 nonzero spots, then the game is over.
    # Note: this only works because None is a "zero" in numpy's eyes.
    elif np.count_nonzero(board) == 9:
        return True

    # Returns false if neither player has won and there are still empty spots on the board.
    return None

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


####### Minimax Algorithm #######

def max_value(board):
    """
    Returns the maximum utility value that a boardstate can provide, along with the action
    """
    # Set the original comparitor value to very low
    v = -999

    # If the board is terminal, return the utility value
    if terminal(board):
        return (utility(board), None)

    # Gets all possible utility values from min
    action_return = list()
    for action in actions(board):
        v_new = max(v, min_value(result(board, action))[0])
        if v_new != v:
            action_return.append(action)
        v = v_new
        if v == 1:
            break

    return (v, action_return[-1])

def min_value(board):
    """
    Returns the minimum utility value that a boardstate can provide, along with the action
    """
    # Set the original comparitor value to very high
    v = 999

    # If the board is terminal, return the utility value
    if terminal(board):
        return (utility(board), None)

    # Gets all possible utility values from max
    action_return = list()
    for action in actions(board):
        v_new = min(v, max_value(result(board, action))[0])
        if v_new != v:
            action_return.append(action)
        v = v_new
        if v == -1:
            break

    return (v, action_return[-1])

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal, then return None
    if terminal(board) == True:
        return None

    # Implement Minimax Algorithm
    if player(board) == "X":
        return max_value(board)[1]
    else:
        return min_value(board)[1]
