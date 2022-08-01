from time import sleep
import pygame as p
import engine
from SmartMoveFinder import get_best_move, find_random

WIDTH = HEIGHT = 512
DIMENSION = 8  # chess board 8*8
SQ_SIZE = HEIGHT // DIMENSION  # square size
MAX_FPS = 15  # for animation
IMAGES = {}


def game_over(screen, txt):
    font = p.font.SysFont('Times New Roman', 25)
    text_renders = font.render(txt, True, (0, 0, 255))
    screen.blit(text_renders, (100, 200))
    for event in p.event.get():
        if event.type == p.QUIT:
            exit()
    p.display.update()
    sleep(15)
    p.quit()


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ",
              "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.State()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move made

    load_images()

    running = True
    sq_selected = ()  # no square is selected (row, col)
    player_clicks = []  # keep track of player clicks

    player_one = True  # human
    player_two = False  # AI
    while running:
        human_turn = (gs.white_to_move and player_one) or (
            not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN and human_turn:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # the user selected the same square twice
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    # append for both 1st and 2nd click
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:  # after 2nd click
                    move = engine.Move(
                        player_clicks[0], player_clicks[1], gs.board)
                    if move.chess_move in valid_moves:
                     #   print(move)
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()  # reset user clicks
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]

                    gs.check_promotion(move.end_row, move.end_col)
        # AI turn
        if not human_turn:
            ai_move = get_best_move(gs)
            gs.make_move(ai_move)
            move_made = True

            gs.check_promotion(ai_move.end_row, ai_move.end_col)

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

        # check end
        if gs.chess_board.outcome() != None:
            text = str(gs.chess_board.outcome().termination).split(".")[1]
            game_over(screen, text)
            running = False


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


main()
