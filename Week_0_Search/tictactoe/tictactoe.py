"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state(): # WORKS
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board): # WORKS
    res = 0
    for row in board:
        for column in row:
            if column != EMPTY:
                res += 1
    if (res % 2) == 0:
        return X
    else:
        return O


def actions(board):
    res = set()
    for r_index, row in enumerate(board):
        for c_index, column in enumerate(row):
            if column == EMPTY:
                res.add((r_index, c_index))
    return res


def result(board, action): # WORKS
    res = copy.deepcopy(board)
    for r_index, row in enumerate(board):
        for c_index, column in enumerate(row):
            if column == EMPTY and r_index == action[0] and c_index == action[1]:
                res[r_index][c_index] = player(board)
                return res  
            elif row == action[0] and column == action[1]:
                raise Exception("Movement Not Valid")
    return res

def winner(board): # WORKS
    var = X
    for _ in range(2):
        for row in board:
            if row == [var, var, var]: # Horizontal
                return var
        if board[0][0] == var and board[1][1] == var and board[2][2] == var: # Diagonal
                return var
        for n in range(3):
            if board[0][n] == var and board[1][n] == var and board[2][n] == var: # Vertical
                    return var
        var = O
    return None


def terminal(board): # WORKS
    if winner(board) != None:
        return True
    res = True
    for row in board:
        for column in row:
            if column == EMPTY:
                res = False
    return res


def utility(board): # WORKS
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        won = winner(board)
        if won == X:
            return 1
        elif won == O:
            return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    possible = actions(board)
    res = (1, None)
    if terminal(board):
        return None
    for action in possible:
        implemented = result(action=action, board=board)
        use = MaxValue(implemented)
        #print(use)
        if use < res[0]:
            res = action
    print(res, use)
    return res

def MaxValue(state):
    if terminal(state):
        return utility(state)
    v = -1000
    for action in actions(state):
        temp = MinValue(result(state, action))
        if v < temp:
            v = temp
    return v

def MinValue(state):
    if terminal(state):
        return utility(state)
    v = 1000
    for action in actions(state):
        temp = MaxValue(result(state, action))
        if v > temp:
            v = temp
    return v