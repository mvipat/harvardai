"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    print("initial_state")
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for row_list in board :
        for cell in row_list :
            if cell == X:
                count_x += 1
            if cell == O:
                count_o += 1
    
    if count_x == 0 and count_o == 0:
        return X
    if count_x <= count_o :
        return X
    
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    print(f"actions board={board}")
    action_list = set()
    index = 0
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if cell is None:
                action_list.add((row,col))
                index += 1

    print(f"action_list={action_list}")
    return action_list

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    print(f"result action={action} board={board}")
    if action is None:
        raise NameError("Invalid Action")
    
    if action[0] < 0 or action[0] > 2:
        raise NameError("Invalid Action")

    if action[1] < 0 or action[1] > 2:
        raise NameError("Invalid Action")
    
    actions(board)

    new_board = list()
    for row,row_list in enumerate(board):
        new_board_row_list = list()
        new_board.append(new_board_row_list)
        for col,cell in enumerate(row_list) :
            new_board_row_list.append(cell)
    
    #print_board(board)

    player_turn = player(new_board)
    print(f"player_turn = {player_turn} action={action} new_board={new_board}")

    for row,row_list in enumerate(new_board):
        for col,cell in enumerate(row_list) :
            if row == action[0] and col == action[1]:
                if cell is not None:
                    raise NameError("Space Not Empty")
                else :
                    new_board[row][col] = player_turn

    print(f"new_board={new_board}")
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Col Winner
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            col_winner = find_col_winner(board,col)
            if col_winner is not None:
                return col_winner

    # Row Winner
    for row,row_list in enumerate(board):
        row_winner = find_row_winner(board,row)
        if row_winner is not None:
            return row_winner

    # Diagonal Winner
    diagonal_winner = find_diagonal_winner(board)
    if diagonal_winner is not None:
        return diagonal_winner
    
    return None

def find_col_winner(board,col_index):
    """Find Col Winer."""
    count_x = 0
    count_o = 0

    #print(f"find_col_winner col_index={col_index}")
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if col == col_index :
                if cell == X:
                    count_x += 1
                elif cell == O:
                    count_o += 1

    if count_x == 3 and count_o == 0:
        return X
    if count_x == 0 and count_o == 3:
        return O
    else :
        return None

def find_row_winner(board,row_index):
    """Find Row Winer."""
    count_x = 0
    count_o = 0

    #print(f"find_row_winner row_index={row_index}")
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if row == row_index :
                if cell == X:
                    count_x += 1
                elif cell == O:
                    count_o += 1

    if count_x == 3 and count_o == 0:
        return X
    if count_x == 0 and count_o == 3:
        return O
    else :
        return None

def find_diagonal_winner(board):
    """Find Diagonal Winner."""

    #print("find_diagonal_winner")

    count_x = 0
    count_o = 0
 
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if row == col :
                if cell == X:
                    count_x += 1
                if cell == O:
                    count_o += 1

    if count_x == 3 and count_o == 0:
        return X
    if count_x == 0 and count_o == 3:
        return O

    count_x = 0
    count_o = 0
 
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if row == 2 - col :
                if cell == X:
                    count_x += 1
                if cell == O:
                    count_o += 1

    if count_x == 3 and count_o == 0:
        return X
    if count_x == 0 and count_o == 3:
        return O
    else :
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    count = 0

    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if cell is None:
                count += 1
    
    if count == 0 :
        return True
    
    if winner(board) is not None:
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    print("utility")
    winner_result = winner(board)
    if winner_result == X:
        return 1
    if winner_result == O:
        return -1
    
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    print("minimax")
    if terminal(board):
        return None
    
    player_turn = player(board)
    print(f"player_turn={player_turn}")
    other_player = None
    if player_turn == X:
        other_player = O
    if player_turn == O:
        other_player = X

    if other_player is None:
        print(board)
        raise NameError("Something wrong with the board")

    if board == initial_state():
        return (1,1)

    turn_row_col = block_other_player(board,other_player)
    if turn_row_col is None:
        aggressive_turn_rol_col1 = play_aggresive(board,player_turn,1)
        if aggressive_turn_rol_col1 is not None:
            return aggressive_turn_rol_col1
        aggressive_turn_rol_col0 = play_aggresive(board,player_turn,0)
        if aggressive_turn_rol_col0 is not None:
            return aggressive_turn_rol_col0
    else :
        return turn_row_col
    
    raise NameError("something broken in minmax ")

def block_other_player(board,other_player):
    """
    Blocks other player from winning
    """
    print(f"block_other_player other_player={other_player}")
    value_find_row_tuple = find_row_tuple(board,other_player,2);
    if value_find_row_tuple is not None:
        return value_find_row_tuple

    value_find_col_tuple = find_col_tuple(board,other_player,2);
    if value_find_col_tuple is not None:
        return value_find_col_tuple

    value_find_dia_tuple = find_diagonal_tuple(board,other_player,2);
    if value_find_dia_tuple is not None:
        return value_find_dia_tuple
            
    value_find_other_dia_tuple = find_other_diagonal_tuple(board,other_player,2);
    if value_find_other_dia_tuple is not None:
        return value_find_other_dia_tuple

    return None

def find_col_tuple(board,player_value,count_block_aggressive):
    """
    Finds Column tuple that should be blocked so that other player doesn't win
    """
    print(f"find_col_tuple count_block_aggressive={count_block_aggressive} player_value={player_value}")
    col_count = [0,0,0]
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if cell == player_value:
                col_count[col] += 1

    print(f"col_count={col_count}")
    col_count_index = 0
    for count in col_count:
        if count == count_block_aggressive:
            return block_column(board,col_count_index)
        
        col_count_index += 1

    return None

def block_column(board,col_index_input):
    """
    Blocks the column so that other place doesn't win
    """
    print(f"block_column col_index_input={col_index_input}")
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if col == col_index_input:
                if cell is None:
                    return (row,col)

    return None

def find_row_tuple(board,player_value,count_block_aggressive):
    """
    Finds Row tuple that should be blocked so that other player doesn't win
    """
    print(f"find_row_tuple count_block_aggressive={count_block_aggressive} player_value={player_value}")
    row_count = [0,0,0]
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if cell == player_value:
                row_count[row] += 1

    print(f"row_count={row_count}")
    row_count_index = 0
    for count in row_count:
        if count == count_block_aggressive:
            col_index = 0
            for row,row_list in enumerate(board):
                for col,cell in enumerate(row_list) :
                    if row == row_count_index:
                        if cell is None:
                            return (row,col)

            col_index += 1

        row_count_index += 1
        
    return None

def find_diagonal_tuple(board,player_value,count_block_aggressive):
    """
    Finds Diagonal tuple that should be blocked so that other player doesn't win
    """
    print(f"find_diagonal_tuple player_valuer={player_value} count_block_aggressive={count_block_aggressive}")
    diagnoal_count = 0
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if row == col and cell == player_value:
                diagnoal_count += 1

    if diagnoal_count == count_block_aggressive:
        for row,row_list in enumerate(board):
            for col,cell in enumerate(row_list) :
                if row == col and cell is None:
                    return (row,col)

def find_other_diagonal_tuple(board,player_value,count_block_aggressive):
    """
    Finds other diagonal tuple that should be blocked so that other player doesn't win
    """
    print(f"find_other_diagonal_tuple player_valuer={player_value} count_block_aggressive={count_block_aggressive}")
    diagnoal_count = 0
    for row,row_list in enumerate(board):
        for col,cell in enumerate(row_list) :
            if col == 2-row and cell == player_value:
                diagnoal_count += 1

    if diagnoal_count == count_block_aggressive:
        for row,row_list in enumerate(board):
            for col,cell in enumerate(row_list) :
                if col == 2-row and cell is None:
                    return (row,col)

def play_aggresive(board,current_player,count):
    """
    Finds tuple that this player should play for winning
    """
    print(f"play_agressive current_player={current_player} count={count}")
    value_find_row_tuple = find_row_tuple(board,current_player,count)
    if value_find_row_tuple is not None:
        return value_find_row_tuple

    value_find_col_tuple = find_col_tuple(board,current_player,count)
    if value_find_col_tuple is not None:
        return value_find_col_tuple

    value_find_dia_tuple = find_diagonal_tuple(board,current_player,count)
    if value_find_dia_tuple is not None:
        return value_find_dia_tuple
            
    value_find_other_dia_tuple = find_other_diagonal_tuple(board,current_player,count)
    if value_find_other_dia_tuple is not None:
        return value_find_other_dia_tuple
    
    return None



