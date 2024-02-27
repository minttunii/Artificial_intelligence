"""
Tic Tac Toe Player
"""


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
    """
    Returns player who has the next turn on a board.
    """
    turns_played = 0
    for row in board:
        for elem in row:
            if elem == O or elem == X:
                turns_played += 1

    # Player X starts the game, so it has the uneven turns
    if turns_played % 2 == 0:
        return X
    # Player O has the even turns
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col] == EMPTY:
                actions.add((row,col))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    j = -1
    i = -1
    if action != None:
        i, j = action

    # Check if i and j are legal values
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise Exception("Action out of range!")
    elif board[i][j] != EMPTY:
        raise Exception("Action is already taken!")

    # Get player in turn to get the correct mark (X or O)
    mark = player(board)

    # Create new board as deepcopy
    new_board = copy.deepcopy(board)

    # Change new board value (i,j)
    new_board[i][j] = mark
    
    return new_board

def checkRows(board):
    "Check rows for winner"  
    for row in board:
        if row.count('X') == len(board):
            return X
        elif row.count('O') == len(board):
            return O
    return None

def checkDiagonals(board):
    "Check diagonals for winner"
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return None

def transpose(board):
    return [
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
    ]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and cols(rows of transpose of the board)
    for check_board in [board, transpose(board)]:
        winner = checkRows(check_board)
        if winner == X or winner == O:
            return winner
         
    # Check diagonals
    winner = checkDiagonals(board)
    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is terminal if either X or O wins or the board is full
    win = winner(board)
    if win == X or win == O:
        return True
    
    # Check if board is full
    num_empty = 0
    for row in board:
        for elem in row:
            if elem == EMPTY:
                num_empty += 1
    
    if num_empty == 0:
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # It is assumed that the board is already terminal
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0
    
def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    best_move = None

    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_move = action

    return v, best_move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    best_move = None

    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_move = action

    return v, best_move

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the board is terminal
    if terminal(board):
        return None
    
    # Get the player in turn
    turn = player(board)

    if turn == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move
