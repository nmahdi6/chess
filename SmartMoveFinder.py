import engine
import random

POSITION_COUNT = 0


def minimax_root(depth, gs, is_maximizing):
    possible_moves = list(gs.get_valid_moves())
    random.shuffle(possible_moves)
    best_move = -9999
    best_move_final = possible_moves[0]

    for pm in possible_moves:
        move = convert_to_Move(gs, pm)
        gs.make_move(move)
        value = minimax(depth - 1, gs, -10000, 10000, not is_maximizing)
        gs.undo_move()
        if(value >= best_move):
            best_move = value
            best_move_final = move
    return best_move_final


def minimax(depth, gs, alpha, beta, is_maximizing):
    global POSITION_COUNT
    POSITION_COUNT += 1

    if(depth == 0):
        return -evaluation(gs)

    possible_moves = list(gs.get_valid_moves())
    random.shuffle(possible_moves)

    if(is_maximizing):
        best_move = -9999
        for x in possible_moves:
            move = convert_to_Move(gs, x)
            gs.make_move(move)
            best_move = max(best_move, minimax(
                depth - 1, gs, alpha, beta, not is_maximizing))
            gs.undo_move()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = 9999
        for x in possible_moves:
            move = convert_to_Move(gs, x)
            gs.make_move(move)
            best_move = min(best_move, minimax(
                depth - 1, gs, alpha, beta, not is_maximizing))
            gs.undo_move()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move


def evaluation(gs):
    total_evaluation = 0
    for i in range(8):
        for j in range(8):
            total_evaluation += get_piece_value(gs.board[i][j])
    return total_evaluation


def get_piece_value(square):
    if(square == "--"):
        return 0
    value = 0
    if square[1] == "p":
        value = 10
    elif square[1] == "N":
        value = 30
    elif square[1] == "B":
        value = 30
    elif square[1] == "R":
        value = 50
    elif square[1] == "Q":
        value = 90
    elif square[1] == 'K':
        value = 900
    value = value if square[0] == "w" else -value

    return value


def get_best_move(gs):
    global POSITION_COUNT
    POSITION_COUNT = 0
    depth = 3
    best_move = minimax_root(depth, gs, True)

    return best_move


def convert_to_Move(gs, move):
    to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    to_rows = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}

    move = move.xboard()
    start_col = to_cols[move[:1]]
    start_row = to_rows[move[1:2]]
    end_col = to_cols[move[2:3]]
    end_row = to_rows[move[3:4]]

    return engine.Move((start_row, start_col), (end_row, end_col), gs.board)


def find_random(gs):
    moves = list(gs.get_valid_moves())
    move = moves[random.randint(0, len(moves) - 1)]
    move = convert_to_Move(gs, move)

    return move
