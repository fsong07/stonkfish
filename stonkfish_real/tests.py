
import os

os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import chess
import chess.engine

WIDTH = 640
HEIGHT = 640
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8

FPS = 60

engine = None
engine_enabled = False

# Board colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (246, 246, 105)
MOVE_COLOR = (100, 180, 100)
BACKGROUND = (30, 30, 30)

# Unicode chess pieces
PIECES = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟"
}

pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess GUI")

clock = pygame.time.Clock()

piece_font = pygame.font.SysFont(
    "dejavusans",
    65
)

text_font = pygame.font.SysFont(
    "arial",
    22
)

board = chess.Board()

selected_square = None
legal_moves = []

move_history = []

engine = None
engine_enabled = False

def draw_board():

    for row in range(8):
        for col in range(8):

            color = LIGHT if (row + col) % 2 == 0 else DARK

            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )

            pygame.draw.rect(screen, color, rect)


def square_to_coordinates(square):

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    x = file * SQUARE_SIZE
    y = (7 - rank) * SQUARE_SIZE

    return x, y


def draw_pieces():

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece is None:
            continue

        x, y = square_to_coordinates(square)

        symbol = PIECES[piece.symbol()]

        color = (
            (255, 255, 255)
            if piece.color == chess.WHITE
            else (20, 20, 20)
        )

        text = piece_font.render(
            symbol,
            True,
            color
        )

        rect = text.get_rect(
            center=(
                x + SQUARE_SIZE // 2,
                y + SQUARE_SIZE // 2
            )
        )

        screen.blit(text, rect)

def draw_highlights():

    if selected_square is None:
        return

    x, y = square_to_coordinates(selected_square)

    pygame.draw.rect(
        screen,
        HIGHLIGHT,
        (x, y, SQUARE_SIZE, SQUARE_SIZE),
        5
    )

    for move in legal_moves:

        if move.from_square == selected_square:

            x, y = square_to_coordinates(
                move.to_square
            )

            center = (
                x + SQUARE_SIZE // 2,
                y + SQUARE_SIZE // 2
            )

            pygame.draw.circle(
                screen,
                MOVE_COLOR,
                center,
                12
            )

def get_square_from_mouse(pos):

    x, y = pos

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    if 0 <= col < 8 and 0 <= row < 8:

        return chess.square(
            col,
            7 - row
        )

    return None


def select_square(square):

    global selected_square
    global legal_moves

    piece = board.piece_at(square)

    if piece and piece.color == board.turn:

        selected_square = square

        legal_moves = [
            move
            for move in board.legal_moves
            if move.from_square == square
        ]

    else:

        selected_square = None
        legal_moves = []


def make_move(from_square, to_square):

    global selected_square
    global legal_moves

    # Find a legal move
    candidates = [
        move for move in board.legal_moves
        if move.from_square == from_square
        and move.to_square == to_square
    ]

    if not candidates:
        return False

    move = candidates[0]

    # Automatically promote to queen
    if board.piece_at(from_square).piece_type == chess.PAWN:

        if chess.square_rank(to_square) in (0, 7):

            move = chess.Move(
                from_square,
                to_square,
                promotion=chess.QUEEN
            )

    move_history.append(board.fen())

    board.push(move)

    selected_square = None
    legal_moves = []

    print("Move:", move.uci())

    return True

# =========================
# GAME STATUS
# =========================

def draw_status():

    if board.is_checkmate():

        message = (
            "Checkmate! "
            + ("Black wins!" if board.turn else "White wins!")
        )

    elif board.is_stalemate():

        message = "Draw: Stalemate"

    elif board.is_insufficient_material():

        message = "Draw: Insufficient material"

    elif board.is_check():

        message = "Check!"

    else:

        message = (
            "White to move"
            if board.turn == chess.WHITE
            else "Black to move"
        )

    pygame.draw.rect(
        screen,
        BACKGROUND,
        (0, 0, WIDTH, 35)
    )

    text = text_font.render(
        message,
        True,
        (255, 255, 255)
    )

    screen.blit(text, (10, 5))

def undo_move():

    if board.move_stack:

        board.pop()

        global selected_square, legal_moves

        selected_square = None
        legal_moves = []


def reset_game():

    global selected_square, legal_moves

    board.reset()

    selected_square = None
    legal_moves = []

    move_history.clear()

running = True

def engine_move():

    if not engine_enabled:
        return

    if board.is_game_over():
        return

    try:
        result = engine.play(
            board,
            chess.engine.Limit(time=0.5)
        )

        board.push(result.move)

        print("Engine move:", result.move.uci())

    except Exception as e:
        print("Engine error:", e)

while running:

    clock.tick(FPS)

    screen.fill(BACKGROUND)

    draw_board()
    draw_highlights()
    draw_pieces()
    draw_status()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # Mouse interaction
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                square = get_square_from_mouse(
                    event.pos
                )

                if square is not None:

                    if selected_square is None:

                        select_square(square)

                    else:

                        success = make_move(
                            selected_square,
                            square
                        )

                        if not success:
                            select_square(square)

                        # Engine responds automatically
                        elif engine_enabled:
                            engine_move()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_u:

                undo_move()

            elif event.key == pygame.K_r:

                reset_game()

            elif event.key == pygame.K_ESCAPE:

                running = False

if engine is not None:

    engine.quit()

pygame.quit()
