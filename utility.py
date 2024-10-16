import random

def evasive(state, player):
    count = sum(row.count(player) for row in state)
    return (count + random.random())

def conqueror(state, player):
    if player == "X":
        count = sum(row.count("O") for row in state)
    else:
        count = sum(row.count("X") for row in state)
    return (0 - count) + random.random()

def defensive(state, player):
    player_count = sum(row.count(player) for row in state)
    opponent_count = sum(row.count('X' if player == 'O' else 'O') for row in state)
    
    return player_count - opponent_count + random.random()

def aggresor(state, player):
    player_count = sum(row.count(player) for row in state)
    opponent_count = sum(row.count('X' if player == 'O' else 'O') for row in state)
    
    return (player_count - opponent_count) * 2 + random.random()