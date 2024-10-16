import copy
import math
import argparse

from utility import evasive, conqueror, defensive, aggresor
from data_struct import Node

def initial_state(rows, columns, rows_of_pieces):
    if rows < 2 or columns < 2:
        raise ValueError("Rows and columns must be at least 2")

    if rows_of_pieces < 1 or rows_of_pieces > rows // 2:
        raise ValueError("Invalid number of rows of pieces")

    state = [["."] * columns for i in range(rows)]  # Initialize the board with zeros

    for r in range(rows_of_pieces):
        for c in range(columns):
            state[r][c] = "X"

    for r in range(rows - rows_of_pieces, rows):
        for c in range(columns):
            state[r][c] = "O"

    return state

def display_state(state):
    lines = [''.join(line) for line in state]
    text = "\n".join(lines)
    print(text)


def goal_test(board_state):
    '''Takes 2D array input and return True if the game is finished'''
    if "O" in board_state[0] or "X" in board_state[len(board_state)-1] or sum(row.count("O") for row in board_state) == 0 or sum(row.count("X") for row in board_state) == 0:
        return True
    
    return False
    
def move_generator(state, player):
    moves = []
    # X moves down array and O moves up array
    if player == "X":
        for i in range(len(state)):
            for j in range(len(state[i])):
                # Check if player occupies square
                if state[i][j] == player:
                    # Check forward move
                    if i+1 < len(state) and state[i+1][j] == '.':
                        moves.append(((i,j), (i+1,j)))
                    # Check diagonal right move
                    if i+1 < len(state) and j-1 >= 0 and (state[i+1][j-1] == 'O' or state[i+1][j-1] == '.'):
                        moves.append(((i,j), (i+1,j-1)))
                    # Check diagonal left move
                    if i+1 < len(state) and j+1 < len(state[i]) and (state[i+1][j+1] == 'O' or state[i+1][j+1] == '.'):
                        moves.append(((i,j), (i+1,j+1)))
    else:
        for i in range(len(state)):
            for j in range(len(state[i])):
                # Check if player occupies square
                if state[i][j] == player:
                    # Check forward move
                    if i-1 >= 0 and state[i-1][j] == '.':
                        moves.append(((i,j), (i-1,j)))
                    # Check diagonal left move
                    if i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'X' or state[i-1][j-1] == '.'):
                        moves.append(((i,j), (i-1,j-1)))
                    # Check diagonal diagonal move
                    if i-1 >= 0 and j+1 < len(state[i]) and (state[i-1][j+1] == 'X' or state[i-1][j+1] == '.'):
                        moves.append(((i,j), (i-1,j+1)))
    return moves

def transition_function(state, move, player):
    # Get coordinates of move
    initial_coord, new_coord = move

    # Create new state using a deep copy of old state
    new_state = copy.deepcopy(state)

    # Make changes to new state
    new_state[initial_coord[0]][initial_coord[1]] = "."
    new_state[new_coord[0]][new_coord[1]] = player

    return new_state

def switch_player(player):
    return ("X" if player == "O" else "O")

def minimax(node, depth, maximizing_player, player, heuristic):
    if depth == 0 or goal_test(node.state):
        return heuristic(node.state, player)

    if maximizing_player:
        max_eval = -math.inf
        for child in node.child:
            eval = minimax(child, depth - 1, False, player, heuristic)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for child in node.child:
            eval = minimax(child, depth - 1, True, player, heuristic)
            min_eval = min(min_eval, eval)
        return min_eval
    

def find_best_move(node, depth, player, heuristic):
    best_move = None
    max_eval = -math.inf
    build_tree(node,heuristic,player,depth)
    for child in node.child:
        eval = minimax(child, depth - 1, False, player, heuristic)
        if eval > max_eval:
            max_eval = eval
            best_move = child.action
    return best_move

def build_tree(node, heuristic, player, depth):
    if depth == 0 or goal_test(node.state):
        return

    for move in move_generator(node.state, player):
        new_state = transition_function(node.state, move, player)
        child = Node(parent=node,state=new_state,action=move, utility=heuristic(new_state, player))
        node.child.append(child)

    for child in node.child:
        build_tree(child, heuristic, switch_player(player), depth - 1)



def play_game(heuristic_white, heuristic_black, board_state, test):
    player = "O"
    # Create head of tree
    node = Node(state=board_state)
    while not goal_test(node.state):
        if player == "O":
            move = find_best_move(node, 3, player, heuristic_white)
        else:
            move = find_best_move(node, 3, player, heuristic_black)
        new_state = transition_function(node.state, move, player)
        if not test:
            display_state(new_state)
            print("------------------")
        node = Node(state=new_state)
        player = switch_player(player)
    return new_state, player

def set_heuristic(argument):
    switcher = {
        'conqueror': conqueror,
        'evasive': evasive,
        'defensive': defensive,
        'aggresor': aggresor
    }
    func = switcher.get(argument)
    return func if func != None else None

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Search a maze for a path')
    parser.add_argument('-r','--rows', help='rows', required=True)
    parser.add_argument('-c','--columns', help='columns', required=True)
    parser.add_argument('-p','--pieces', help='pieces', required=True)
    parser.add_argument('-w','--white_heuristic', help='white_heuristic', required=True)
    parser.add_argument('-b','--black_heuristic', help='black_heuristic', required=True)
    parser.add_argument('-t','--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    rows = int(args.rows)
    columns = int(args.columns)
    pieces = int(args.pieces)

    heuristic_white = set_heuristic(args.white_heuristic)
    heuristic_black = set_heuristic(args.black_heuristic)

    if heuristic_black is None:
        raise ValueError("Invalid heuristic for black")
    if heuristic_white is None:
        raise ValueError("Invalid heuristic for white")
    
    test = False
    if args.test:
        test = True

    board = initial_state(rows,columns,pieces)

    # Play game returns the loser as the player is switched before the state is returned
    final_state, loser = play_game(heuristic_white, heuristic_black, board, test)
    winner = switch_player(loser)

    if test:
        print(winner)
    else:
        display_state(final_state)
        print(f"Winner is: {winner}")