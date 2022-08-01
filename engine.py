import chess


class State:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.chess_board = chess.Board()
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move  # swap players

        self.chess_board.push(move.chess_move)

    def undo_move(self):
        if len(self.move_log) != 0:  # make sure there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # switch turns back

            self.chess_board.pop()

    def get_valid_moves(self):
        return self.chess_board.legal_moves

    def check_promotion(self, i, j):
        cols_to = {0: "a", 1: "b", 2: "c", 3: "d",
                   4: "e", 5: "f", 6: "g", 7: "h"}
        row_to = {0: "8", 1: "7", 2: "6", 3: "5",
                  4: "4", 5: "3", 6: "2", 7: "1"}

        square = self.board[i][j]

        if square[1] == "p":
            chess_square = (str(row_to[0]) + str(cols_to[7]))[::-1]
            chess_square_number = chess.parse_square(chess_square)

            if square[0] == "w" and i == 0:
                self.board[i][j] = "wQ"
                self.chess_board.set_piece_at(
                    chess.Square(chess_square_number), chess.Piece.from_symbol("Q"))
            elif square[0] == "b" and i == 7:
                self.board[i][j] = "bQ"
                self.chess_board.set_piece_at(
                    chess.Square(chess_square_number), chess.Piece.from_symbol("Q"))


class Move:
    cols_to = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    row_to = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        self.chess_piece_moved = self.cols_to[self.start_col] + \
            self.row_to[self.start_row]
        self.chess_piece_captured = self.cols_to[self.end_col] + \
            self.row_to[self.end_row]

        self.chess_move = chess.Move.from_uci(
            self.chess_piece_moved + self.chess_piece_captured)

    def __str__(self):
        return self.piece_moved + "," + self.piece_captured
