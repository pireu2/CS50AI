"""
Tic Tac Toe Player
"""

import math
import copy

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
    
    if board == [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]:
        return X
    else:
        count_x = 0
        count_o = 0
        for row in board:
            for i in row:
                if i == X:
                    count_x += 1
                elif i == O:
                    count_o += 1
        if count_x > count_o:
            return O
        else:
            return X




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    list = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                list.append((i,j))

    return list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)

    board_copy[action[0]][action[1]] = player(board_copy)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        #check rows
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        #check collumns
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
        
    #diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0] 
    if board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]

    return None   


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    p = player(board)
    if p == X:
        move = max_value(board)[1]
        return move
    elif p == O:
        move = min_value(board)[1]
        return move
        
    
def max_value(state):
    if terminal(state):
        return utility(state), None
    v = -math.inf
    move = None
    for action in actions(state):
        test = min_value(result(state,action))[0]
        if test > v:
            v = test
            move = action
    return v, move

def min_value(state):
    if terminal(state):
        return utility(state), None
    v = math.inf
    move = None
    for action in actions(state):
        test = max_value(result(state,action))[0]
        if test < v:
            v = test
            move = action
    return v, move

if __name__ == "__main__":
    board = [[X, X, EMPTY],
            [O, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    print(minimax(board))
