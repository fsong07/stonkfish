
import pygame
import chess
import sys

# ==========================================
# CONFIGURATION
# ==========================================

WIDTH = 800
HEIGHT = 800

BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8

OFFSET_X = (WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2

FPS = 60

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)

SELECTED_COLOR = (246, 246, 105)
MOVE_COLOR = (80, 180, 80)
BACKGROUND = (35, 35, 35)

TEXT_COLOR = (255, 255, 255)

# Chess piece symbols
PIECES = {
    "K": "♔",
    "Q": "♕",
    "R": "♖",
    "B": "♗",
    "N": "♘",
    "P": "♙",
    "k": "♚",
    "q": "♛",
    "r": "♜",
    "b": "♝",
    "n": "♞",
    "p": "♟",
}


# ==========================================
# INITIALIZATION
# ==========================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine GUI")

clock = pygame.time.Clock()

piece_font = pygame.font.SysFont(
    "DejaVu Sans",
    68
)

text_font = pygame.font.SysFont(
    "Arial",
    24
)


# ==========================================
# GAME STATE
# ==========================================

board = chess.Board()

selected_square = None
legal_moves = []

move_history = []


# ==========================================
# BOARD COORDINATES
# ==========================================

def square_to_screen(square):
    """
    Convert a python-chess square index
    into screen coordinates.
    """

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    x = OFFSET_X + file * SQUARE_SIZE
    y = OFFSET_Y + (7 - rank) * SQUARE_SIZE

    return x, y


def screen_to_square(pos):
    """
    Convert mouse coordinates into
    a python-chess square index.
    """

    x, y = pos

    file = (x - OFFSET_X) // SQUARE_SIZE
    rank = 7 - ((y - OFFSET_Y) // SQUARE_SIZE)

    if not (0 <= file < 8 and 0 <= rank < 8):
        return None

    return chess.square(file, rank)


# ==========================================
# DRAW CHESSBOARD
# ==========================================

def draw_board():

    for rank in range(8):
        for file in range(8):

            x = OFFSET_X + file * SQUARE_SIZE
            y = OFFSET_Y + rank * SQUARE_SIZE

            if (rank + file) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE

            pygame.draw.rect(
                screen,
                color,
                (x, y, SQUARE_SIZE, SQUARE_SIZE)
            )


# ==========================================
# HIGHLIGHT SQUARES
# ==========================================

def draw_highlights():

    # Selected square
    if selected_square is not None:

        x, y = square_to_screen(selected_square)

        pygame.draw.rect(
            screen,
            SELECTED_COLOR,
            (x, y, SQUARE_SIZE, SQUARE_SIZE)
        )

    # Legal move destinations
    for move in legal_moves:

        target = move.to_square
        x, y = square_to_screen(target)

        center = (
            x + SQUARE_SIZE // 2,
            y + SQUARE_SIZE // 2
        )

        if board.piece_at(target):

            pygame.draw.circle(
                screen,
                MOVE_COLOR,
                center,
                SQUARE_SIZE // 2 - 5,
                5
            )

        else:

            pygame.draw.circle(
                screen,
                MOVE_COLOR,
                center,
                12
            )


# ==========================================
# DRAW PIECES
# ==========================================

def draw_pieces():

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece is None:
            continue

        symbol = PIECES[piece.symbol()]

        x, y = square_to_screen(square)

        image = piece_font.render(
            symbol,
            True,
            (255, 255, 255) if piece.color else (20, 20, 20)
        )

        rect = image.get_rect(
            center=(
                x + SQUARE_SIZE // 2,
                y + SQUARE_SIZE // 2
            )
        )

        screen.blit(image, rect)


# ==========================================
# BOARD LABELS
# ==========================================

def draw_coordinates():

    for i in range(8):

        # Files
        file_text = text_font.render(
            chess.FILE_NAMES[i],
            True,
            TEXT_COLOR
        )

        screen.blit(
            file_text,
            (
                OFFSET_X + i * SQUARE_SIZE + 5,
                OFFSET_Y + BOARD_SIZE + 5
            )
        )

        # Ranks
        rank_text = text_font.render(
            str(8 - i),
            True,
            TEXT_COLOR
        )

        screen.blit(
            rank_text,
            (
                OFFSET_X - 22,
                OFFSET_Y + i * SQUARE_SIZE + 5
            )
        )


# ==========================================
# GAME STATUS
# ==========================================

def draw_game_status():

    if board.is_checkmate():

        winner = "Black" if board.turn else "White"
        message = f"Checkmate! {winner} wins."

    elif board.is_stalemate():

        message = "Draw by stalemate."

    elif board.is_insufficient_material():

        message = "Draw: insufficient material."

    elif board.is_check():

        message = "Check!"

    else:

        message = (
            "White to move"
            if board.turn
            else "Black to move"
        )

    text = text_font.render(
        message,
        True,
        TEXT_COLOR
    )

    screen.blit(text, (20, 20))


# ==========================================
# DRAW EVERYTHING
# ==========================================

def draw():

    screen.fill(BACKGROUND)

    draw_board()
    draw_highlights()
    draw_pieces()
    draw_coordinates()
    draw_game_status()

    pygame.display.flip()


# ==========================================
# MOVE GENERATION
# ==========================================

def get_legal_moves(square):

    return [
        move
        for move in board.legal_moves
        if move.from_square == square
    ]


# ==========================================
# MOVE EXECUTION
# ==========================================

def make_move(move):

    if move not in board.legal_moves:
        return

    move_history.append(board.fen())

    board.push(move)

    global selected_square, legal_moves

    selected_square = None
    legal_moves = []


# ==========================================
# MOUSE INPUT
# ==========================================

def handle_click(pos):

    global selected_square, legal_moves

    square = screen_to_square(pos)

    if square is None:
        return

    # Select a piece
    if selected_square is None:

        piece = board.piece_at(square)

        if piece and piece.color == board.turn:

            selected_square = square
            legal_moves = get_legal_moves(square)

        return

    # Find moves to the clicked square
    candidates = [
        move
        for move in legal_moves
        if move.to_square == square
    ]

    if candidates:

        # Handle pawn promotion
        if len(candidates) > 1:

            global promotion_moves
            promotion_moves = candidates
            return

        make_move(candidates[0])
        return

    # Select another friendly piece
    piece = board.piece_at(square)

    if piece and piece.color == board.turn:

        selected_square = square
        legal_moves = get_legal_moves(square)

    else:

        selected_square = None
        legal_moves = []


# ==========================================
# PROMOTION
# ==========================================

promotion_moves = []


def handle_promotion(key):

    promotion_map = {
        pygame.K_q: chess.QUEEN,
        pygame.K_r: chess.ROOK,
        pygame.K_b: chess.BISHOP,
        pygame.K_n: chess.KNIGHT
    }

    if key not in promotion_map:
        return

    chosen_piece = promotion_map[key]

    for move in promotion_moves:

        if move.promotion == chosen_piece:

            make_move(move)
            break

    promotion_moves.clear()

# ==========================================
# FUTURE ENGINE INTERFACE
# ==========================================

def get_engine_move():

    """
    Future chess engine integration.

    The engine will receive the current board
    and return a legal chess move.

    Example:

        move = engine.search(board)
        make_move(move)
    """

    pass


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and not promotion_moves:
                handle_click(event.pos)

        elif event.type == pygame.KEYDOWN:

            if promotion_moves:

                handle_promotion(event.key)

    draw()

pygame.quit()
sys.exit()
