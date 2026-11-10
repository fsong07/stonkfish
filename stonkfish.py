#===================
#Import & Initialize
#===================

#Import libraries
import chess
import pygame
import sys

#Initialize pygame
pygame.init()

#=============
#Configuration
#=============

#Window Size
WIDTH = 1000
HEIGHT = 1000

#Board & Square Size
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8

#Margin Size
X_MARGIN = (WIDTH - BOARD_SIZE) / 2
Y_MARGIN = (HEIGHT - BOARD_SIZE) / 2

#Square Colour
LIGHT_SQUARE_COLOUR = (233, 246, 225)
DARK_SQUARE_COLOUR = (125, 200, 100)

#Highlights
SELECTED_SQUARE_HL = (172, 225, 255)
LEGAL_MOVES_HL = (172, 225, 255)
CHECK_SQUARE_HL = (250, 135, 135)

#UI Colour
BG_COLOUR = (100, 160, 100)
TEXT_COLOUR = (233, 246, 225)

#Load Chess Pieces
PIECES = {
    "K": (pygame.transform.smoothscale(pygame.image.load('white_king.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "Q": (pygame.transform.smoothscale(pygame.image.load('white_queen.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "R": (pygame.transform.smoothscale(pygame.image.load('white_rook.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "B": (pygame.transform.smoothscale(pygame.image.load('white_bishop.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "N": (pygame.transform.smoothscale(pygame.image.load('white_knight.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "P": (pygame.transform.smoothscale(pygame.image.load('white_pawn.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "k": (pygame.transform.smoothscale(pygame.image.load('black_king.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "q": (pygame.transform.smoothscale(pygame.image.load('black_queen.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "r": (pygame.transform.smoothscale(pygame.image.load('black_rook.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "b": (pygame.transform.smoothscale(pygame.image.load('black_bishop.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "n": (pygame.transform.smoothscale(pygame.image.load('black_knight.png'), (SQUARE_SIZE, SQUARE_SIZE))),
    "p": (pygame.transform.smoothscale(pygame.image.load('black_pawn.png'), (SQUARE_SIZE, SQUARE_SIZE))),
}

#Assign pieces a piece-square tables
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MG_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

KING_EG_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

#Define the FEN for the position
FEN = ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

#Define which side the engine plays as
TURN = chess.BLACK

#Frames per Second
FPS = 60

#======
#Screen
#======

#Set 'screen' to initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Rename the screen
pygame.display.set_caption("stonkfish")

#Set the font and size
font = pygame.font.SysFont("Bahnschrift", 30)

#Function that will draw the screen
def draw_screen():

    #Fill the screen with the background colour constant
    screen.fill(BG_COLOUR)

#===================
#Initial Game Status
#===================

#Use python-chess to create a chess board with the starting FEN
board = chess.Board()

#No selected squares
selected_square = None

#No legal moves or move history yet
legal_moves = []
move_history = []

#=====================
#Coordinates Converter
#=====================

#Function that converts board coordinates to screen coordinates
def square_screen(square):

    #Define files and ranks using python-chess
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    #Calculate the location of pixels using previously defined constants given that pygame's pizels start at the top-left corner
    screen_x = X_MARGIN + file * SQUARE_SIZE
    screen_y = Y_MARGIN + (7 - rank) * SQUARE_SIZE

    #Return the location of the x and y pixels
    return screen_x, screen_y

#Function that converts screen coordinates to board coordinates
def screen_square(screen):

    #Define the location of pixels using pygame
    screen_x, screen_y = screen

    #Calculate the file and rank from the location of pixels using previously defined constants given that pygame's pizels start at the top-left corner
    file = int((screen_x - X_MARGIN) // SQUARE_SIZE)
    rank = int(7 - ((screen_y - Y_MARGIN) // SQUARE_SIZE))

    #If statement that filters out if location of pixel is not on the board
    if not (0 <= file < 8 and 0 <= rank < 8):
        return None

    #Return the file and rank values
    else:
        return chess.square(file, rank)

#==========
#Draw Board
#==========

#Function that will draw the board
def draw_board():

    #For loop that defines 8 files and ranks
    for file in range(8):
        for rank in range(8):

            #Define the position of the squares
            square_position_x = X_MARGIN + file * SQUARE_SIZE
            square_position_y = Y_MARGIN + rank * SQUARE_SIZE

            #Calculate whether a square is a light square or dark square
            if (rank + file) % 2 == 0:
                square_colour = LIGHT_SQUARE_COLOUR
            else:
                square_colour = DARK_SQUARE_COLOUR

            #Use pygame to draw a squares that make a board
            pygame.draw.rect(screen, square_colour, (square_position_x, square_position_y, SQUARE_SIZE, SQUARE_SIZE))


#Function that will draw the board coordinates
def draw_coordinates():

    #For loop that runs 8 times for 8 files and ranks
    for i in range(8):

        #Define the text and font
        file_coordinate_text = font.render(chess.FILE_NAMES[i], True, TEXT_COLOUR)
        rank_coordinate_text = font.render(str(8 - i), True, TEXT_COLOUR)

        #Draw the text by calculating the positions of the text and the text and font
        screen.blit(file_coordinate_text, (X_MARGIN + i * SQUARE_SIZE + 40, Y_MARGIN + BOARD_SIZE + 18))
        screen.blit(rank_coordinate_text, (X_MARGIN - 40, Y_MARGIN + i * SQUARE_SIZE + 40))

#===========
#Draw Pieces
#===========

#Function that will draw the pieces
def draw_pieces():

    #For loop that goes through all squares
    for square in chess.SQUARES:

        #Define that a piece is at a square
        piece = board.piece_at(square)

        #If statement that states that if a piece is not on a sqaure, to continue
        if piece is None:
            continue

        #Define that a piece is the image loaded on the constant
        piece = PIECES[piece.symbol()]

        #Convert the square coordinates to a screen coordinate
        piece_x, piece_y = square_screen(square)

        #Get the centre of the square
        centre = piece.get_rect(center = (piece_x + SQUARE_SIZE / 2, piece_y + SQUARE_SIZE / 2))

        #Make the images appear on screen
        screen.blit(piece, centre)

#======================
#Draw Square Highlights
#======================

#Function that will draw square highlights
def draw_highlights():

    #If statement that checks that there is a selected square
    if selected_square is not None:

        #Converts the selected square coordinates to screen coordinates
        selected_square_x, selected_square_y = square_screen(selected_square)
        
        #Draws a rectangle that covers the selected square
        pygame.draw.rect(screen, SELECTED_SQUARE_HL, (selected_square_x, selected_square_y, SQUARE_SIZE, SQUARE_SIZE))

    #For loop that looks at moves in all legal moves
    for move in legal_moves:

        #Defines a destination square as a movable square
        destination_square = move.to_square

        #Converts the destination square coordinates to screen coordinates
        destination_square_x, destination_square_y = square_screen(destination_square)

        #Finds the centre of the destination square
        centre = (destination_square_x + SQUARE_SIZE / 2, destination_square_y + SQUARE_SIZE / 2)

        #If statement that checks if there is a capturable piece in the destination square
        if board.piece_at(destination_square):
            #Draws a circle around the square to avoid overlapping textures
            pygame.draw.circle(screen, LEGAL_MOVES_HL, centre, SQUARE_SIZE / 2 - 5, 5)

        #If statement for when there is no capturable piece in the destination square
        else:
            #Draws a circle in the centre of the square
            pygame.draw.circle(screen, LEGAL_MOVES_HL, centre, 12)

    #If statement that checks if there is a check in the position
    if board.is_check():

        #Defines the square that has the king being checked
        check_square = board.king(board.turn)

        #Converts the check square coordinates to screen coordinates
        check_square_x, check_square_y = square_screen(check_square)

        #If statement that draws the check highlight if there is a piece on the square
        if check_square is not None:
            pygame.draw.rect(screen, CHECK_SQUARE_HL, (check_square_x, check_square_y, SQUARE_SIZE, SQUARE_SIZE))

#==========
#Evaluation
#==========

#Function that will assign values to outcomes
def evaluator(position):

    #Assign the white evaluation as the sum of the material of white
    white_material = count_material(position, chess.WHITE)
    #Assign the black evaluation as the sum of the material of black
    black_material = count_material(position, chess.BLACK)
    #Assign the material as the difference between the white material and black material
    material = white_material - black_material

    #Find the evaluation of the position
    evaluation = material + piece_square_value(position)

    #Return the evaluation
    return evaluation

#Function that will count material depending on which side and what position it is
def count_material(position, side):

    #Assign material value to 0
    material = 0

    #Adds to material value depending on the quantity and value
    material += len(position.pieces(chess.PAWN, side)) * 100
    material += len(position.pieces(chess.KNIGHT, side)) * 300
    material += len(position.pieces(chess.BISHOP, side)) * 300
    material += len(position.pieces(chess.ROOK, side)) * 500
    material += len(position.pieces(chess.QUEEN, side)) * 900

    #Returns material
    return material

#Function that will determine piece value
def piece_value(piece):

    #Define piece values using a dictionary
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 6741
    }

    #Determine the piece type
    piece_type = piece.piece_type

    #Draw from the dictionary to get the value
    piece_value = piece_values[piece_type]

    #Return the piece value
    return piece_value

#Function that changes the value of pieces depending on their positions on the board
def piece_square_value(position):

    #If statement that checks if the queens are off the board and the material count is less than 1300
    if ((bool(position.pieces(chess.QUEEN, chess.WHITE)) == False and bool(position.pieces(chess.QUEEN, chess.BLACK)) == False)) and (count_material(position, chess.WHITE) + count_material(position, chess.BLACK)) <= 1300:

        #Assigns all pieces relative values using their respective piece-value tables for white and black
        pawn_rvalue = sum([PAWN_TABLE [i] for i in position.pieces(chess.PAWN, chess.WHITE)])
        pawn_rvalue -= sum([PAWN_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.PAWN, chess.BLACK)])
        knight_rvalue = sum([KNIGHT_TABLE [i] for i in position.pieces(chess.KNIGHT, chess.WHITE)])
        knight_rvalue -= sum([KNIGHT_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_rvalue = sum([BISHOP_TABLE [i] for i in position.pieces(chess.BISHOP, chess.WHITE)])
        bishop_rvalue -= sum([BISHOP_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.BISHOP, chess.BLACK)])
        rook_rvalue = sum([ROOK_TABLE [i] for i in position.pieces(chess.ROOK, chess.WHITE)])
        rook_rvalue -= sum([ROOK_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.ROOK, chess.BLACK)])
        queen_rvalue = sum([QUEEN_TABLE [i] for i in position.pieces(chess.QUEEN, chess.WHITE)])
        queen_rvalue -= sum([QUEEN_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.QUEEN, chess.BLACK)])
        #Assigns the king the endgame piece-value table
        king_rvalue = sum([KING_EG_TABLE [i] for i in position.pieces(chess.KING, chess.WHITE)])
        king_rvalue -= sum([KING_EG_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.KING, chess.BLACK)])

    #If statement that checks if the queens are on the board or the material count is more than 1300
    else:

        #Assigns all pieces relative values using their respective piece-value tables for white and black
        pawn_rvalue = sum([PAWN_TABLE [i] for i in position.pieces(chess.PAWN, chess.WHITE)])
        pawn_rvalue -= sum([PAWN_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.PAWN, chess.BLACK)])
        knight_rvalue = sum([KNIGHT_TABLE [i] for i in position.pieces(chess.KNIGHT, chess.WHITE)])
        knight_rvalue -= sum([KNIGHT_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_rvalue = sum([BISHOP_TABLE [i] for i in position.pieces(chess.BISHOP, chess.WHITE)])
        bishop_rvalue -= sum([BISHOP_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.BISHOP, chess.BLACK)])
        rook_rvalue = sum([ROOK_TABLE [i] for i in position.pieces(chess.ROOK, chess.WHITE)])
        rook_rvalue -= sum([ROOK_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.ROOK, chess.BLACK)])
        queen_rvalue = sum([QUEEN_TABLE [i] for i in position.pieces(chess.QUEEN, chess.WHITE)])
        queen_rvalue -= sum([QUEEN_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.QUEEN, chess.BLACK)])
        #Assigns the king the endgame piece-value table
        king_rvalue = sum([KING_MG_TABLE [i] for i in position.pieces(chess.KING, chess.WHITE)])
        king_rvalue -= sum([KING_MG_TABLE [chess.square_mirror(i)] for i in position.pieces(chess.KING, chess.BLACK)])

    #Adds all values to get the board value
    board_value = pawn_rvalue + knight_rvalue + bishop_rvalue + rook_rvalue + queen_rvalue + king_rvalue

    #Returns board value
    return board_value

#===============
#Draw Game State
#===============

#Function that will draw the game status
def draw_status():

    #If statement that checks if the board has checkmate
    if board.is_checkmate():

        #If statement that checks the turn, and outputs a message that says which side wins
        if board.turn == chess.BLACK:
            message = "White Wins!"
        else:
            message = "Black Wins!"

    #If statement that checks if the board has stalemate
    elif board.is_stalemate():

        #Message that shows the result
        message = "Draw: Stalemate"

    #If statement that checks if the board has insufficient material
    elif board.is_insufficient_material():

        #Message that shows the result
        message = "Draw: Insufficient Material"

    #If statement that checks if the board has reached the fifty move rule
    elif board.is_fifty_moves():

        #Message that shows the result
        message = "Draw: Fifty Move Rule"

    #If statement that checks if the board has reached three-fold repetition
    elif board.is_repetition():

        #Message that shows the result
        message = "Draw: Three-Fold Repetition"

    #If statement that checks whose turn it is
    else:

        #If statement that checks the turn, and outputs a message that says which side should move
        if board.turn == chess.WHITE:
            message = "White to move:"
        else:
            message = "Black to move:"

    #Define the text message and colour
    status_text = font.render(message, True, TEXT_COLOUR)

    #Prints out the text
    screen.blit(status_text, (100, 50))

#=============
#Draw Function
#=============

#Function that will draw everything
def draw():

    #Calls all functions so that the draw() function will draw all draw functions
    draw_screen()
    draw_board()
    draw_coordinates()
    draw_highlights()
    draw_pieces()
    draw_status()

    #Updates the display so screen will draw and update
    pygame.display.flip()

#===================
#Promotion Selection
#===================

#Defines promotion moves as a list
promotion_moves = []

#Function that will allow for promotion with keys
def promotion_input(input):

    #Maps what inputs will promote to what piece
    promotion_inputs = {
        pygame.K_q: chess.QUEEN,
        pygame.K_r: chess.ROOK,
        pygame.K_b: chess.BISHOP,
        pygame.K_n: chess.KNIGHT
    }

    #If statement that will do nothing if any other key than a promotion input is pressed
    if input not in promotion_inputs:
        return

    #Defines the promotion piece by the input
    promotion_piece = promotion_inputs[input]

    #For loop for all moves in promotion moves
    for move in promotion_moves:

        #If statement that checks if the promotion move is the piece chosen
        if move.promotion == promotion_piece:

            #Makes the promotion move
            make_move(move)
            break

    #Removes all promotion input keys until next promotion event
    promotion_moves.clear()

#===========
#Mouse Input
#===========

#Function that will take mouse click inputs
def click_input(input):

    #Changes selected_square and legal moves
    global selected_square, legal_moves

    #Converts the clicked square coordinates to screen coordinates
    clicked_square = screen_square(input)

    #If statement that returns nothing when there is no square clicked
    if clicked_square is None:
        return

    #If statement for when there is no square selected
    if selected_square is None:

        #Define the piece as a piece at a clicked square
        piece = board.piece_at(clicked_square)

        #If statement for when the clicked square piece colour is the same as the colour that must move
        if piece and piece.color == board.turn:

            #Square is clickable
            selected_square = clicked_square

            #Gets all legal moves from the clicked square
            legal_moves = get_legal_moves(clicked_square)

        return

    #Define candidate moves as all moves that are legal and are from the clicked square
    candidate_moves = [
        move
        for move in legal_moves
        if move.to_square == clicked_square
    ]

    #If statement if there are candidate moves
    if candidate_moves:

        #If statement for when there are more than 1 candidate move
        if len(candidate_moves) > 1:

            #Changes promotion moves
            global promotion_moves

            #Make promotion moves part of candidate moves
            promotion_moves = candidate_moves

            return

        #Make a move if there are no other candidate moves
        make_move(candidate_moves[0])

        return

    #Define a piece as a piece on the clicked square
    piece = board.piece_at(clicked_square)

    #If statement for when the clicked square piece colour is the same as the colour that must move
    if piece and piece.color == board.turn:

        #Square is clickable
        selected_square = clicked_square

        #Gets all legal moves from the clicked square
        legal_moves = get_legal_moves(clicked_square)

    #If statement for when the clicked square piece colour is not the same as the colour that must move 
    else:

        #Defines selected square and legal moves as none
        selected_square = None
        legal_moves = []

#==========
#Make Moves
#==========

#Function that will get all legal moves
def get_legal_moves(moves):

    #Returns all legal moves that are generated by python-chess if the move is from a square
    return [
        move
        for move in board.legal_moves
        if move.from_square == moves
    ]

#Function that will make a move
def make_move(move):

    #If statement that checks if the move is legal and passes if the move is not
    if move not in board.legal_moves:
        return

    #Adds move to move history and FEN
    move_history.append(board.fen())

    #Makes move on the board
    board.push(move)

    #Changes selected square and legal moves
    global selected_square, legal_moves

    #Defines selected square and legal moves after the move
    selected_square = None
    legal_moves = []

#=================
#Minimax Algorithm
#=================

#Function that defines and calls minimax
def minimax(position, depth, maximizing_player, alpha, beta):

    #If statement that checks if the game is over by checkmate and returns the evaluation of the position
    if position.is_checkmate():
        if maximizing_player:
            return float('-inf')
        else:
            return float('inf')
        
    #If statement that checks if the game is over by draw and returns the evaluation of the position
    if position.is_game_over(claim_draw = True):
        return 0

    #If statement that checks if the game is over and returns the evaluation of the position
    if depth <= 0:
        return evaluator(position)

    #Defines and gets a list of all ordered moves
    ordered_moves = sorted(position.legal_moves, key = lambda move: order_moves(move, position), reverse = True)

    #If statement for if it's the maximizing player's turn
    if maximizing_player:

        #State the maximum possible evaluation (7749 is M1 representing Mate in 1 in binary)
        max_evaluation = float('-inf')

        #For loop that runs for all legal moves
        for move in ordered_moves:

            #Makes the move
            position.push(move)
            #Evaluates the move by calling on minimax
            evaluation = minimax(position, depth - 1, False, alpha, beta)

            #Undos the move
            position.pop()

            #Compares which evaluation is higher and defines max evaluation as the said highest value
            max_evaluation = max(max_evaluation, evaluation)

            #Compares which evaluation is higher and defines alpha as the said highest value
            alpha = max(alpha, evaluation)
            #If statement that allows child to be pruned if the evaluation of a certain position is bigger than beta
            if beta <= alpha:
                break

        #Returns the highest evaluation
        return max_evaluation

    #If statement for if it's the minimizing player's turn
    else:

        #State the maximum possible evaluation (-7749 is -M1 representing Mate in 1 for Black in binary)
        min_evaluation = float('inf')

        #For loop that runs for all legal moves
        for move in ordered_moves:

            #Makes the move
            position.push(move)
            #Evaluates the move by calling on minimax
            evaluation = minimax(position, depth - 1, True, alpha, beta)
            #Undos the move
            position.pop()

            #Compares which evaluation is lower and definesmin evaluation as the said lowest value
            min_evaluation = min(min_evaluation, evaluation)

            #Compares which evaluation is higher and defines beta as the said highest value
            beta = min(beta, evaluation)
            #If statement that allows child to be pruned if the evaluation of a certain position is bigger than alpha
            if beta <= alpha:
                break

        #Returns the lowest evaluation
        return min_evaluation

#Function that will assign a move to the evaluation in the minimax algorithm
def move_picker(position, depth, maximizing_player, alpha, beta):

    #If statement that defines the max evaluation based on whose turn it is
    if maximizing_player:
        max_evaluation = float('-inf')
    else:
        max_evaluation = float('inf')

    #States there is no final move yet
    final_move = None

    #Defines and gets a list of all ordered moves
    ordered_moves = sorted(position.legal_moves, key = lambda move: order_moves(move, position), reverse = True)

    #For loop that runs for all ordered moves
    for move in ordered_moves:

        #Makes the move
        position.push(move)
        #Evaluates the move by calling on minimax
        evaluation = minimax(position, depth - 1, not maximizing_player, alpha, beta)
        #Undos the move
        position.pop()

        #If statement that determines evaluation and final move based on whose turn it is
        if maximizing_player:

            #If statement that checks if the evaluation of a move is better than the worst case scenario
            if evaluation > max_evaluation:

                #Defines the evaluation of the best move in the minimax search than the worst case scenario as the new worst case scenario
                max_evaluation = evaluation

                #Defines the final move as the best move in the minimax search
                final_move = move

            #Compares which evaluation is higher and defines alpha as the said highest value
            alpha = max(alpha, evaluation)
            #If statement that allows child to be pruned if the evaluation of a certain position is bigger than beta
            if beta <= alpha:
                break

        #If statement that determines evaluation and final move based on whose turn it is
        else:

            #If statement that checks if the evaluation of a move is worse (so better for the minimizing player) than the worst case scenario
            if evaluation < max_evaluation:

                #Defines the evaluation of the best move in the minimax search than the worst case scenario as the new worst case scenario
                max_evaluation = evaluation

                #Defines the final move as the best move in the minimax search
                final_move = move

            #Compares which evaluation is higher and defines beta as the said highest value
            beta = min(beta, evaluation)
            #If statement that allows child to be pruned if the evaluation of a certain position is bigger than alpha
            if beta <= alpha:
                break

    #Returns the final move
    return final_move

#Function that will make the final move
def minimax_move_maker(position):

    #If statement that checks that the game is not over and it
    if not position.is_game_over() and position.turn == TURN:

        #Defines that a maximizing player is when it's their turn
        maximizing_player = TURN == chess.WHITE

        #Finds the final move using the move picker function
        final_move = move_picker(position, 3, maximizing_player, float('-inf'), float('inf'))

        #If statement that checks if there is a final move and makes it
        if final_move:
            make_move(final_move)

#Function that will order the moves
def order_moves(move, position):

    #Give the move priority score 0
    move_priority = 0

    #Assign attacked piece and attacking piece a piece type
    attacked_piece = position.piece_at(move.to_square)
    attacking_piece = position.piece_at(move.from_square)

    #If statement that checks for captures
    if position.is_capture(move):

        #If statement that checks for en passant, and gives a value of a pawn if so
        if attacked_piece is None:
            attacked_piece = chess.Piece(chess.PAWN, not position.turn)

        #Assigns move priority to a score based on the value of the attacked and attacking piece
        move_priority = 10 * piece_value(attacked_piece) - piece_value(attacking_piece)

    #If statement that checks for promotions
    if move.promotion:

        #Assigns promoted piece a piece type
        promoted_piece = chess.Piece(move.promotion, position.turn)

        #Assigns move priority to a score based on the value of the promoted piece and pawn promoted
        move_priority += piece_value(promoted_piece) - piece_value(chess.Piece(chess.PAWN, position.turn))

    #Return move priority
    return move_priority

#=========
#Main Loop
#=========

#Initialize clock
clock = pygame.time.Clock()

#Attribute running to true or false
running = True

#while loop that is running for running = True
while running:

    #Clocks ticks by the assigned framerate
    clock.tick(FPS)

    #For loop that looks at events
    for event in pygame.event.get():

        #If statement that will quit the program if event is quitting
        if event.type == pygame.QUIT:
            running = False

        #If statement that checks for mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:

            #If statement that defines the input as a click input if there was an event that was not a promotion
            if event.button == 1 and not promotion_moves:
                click_input(event.pos)

        #If statement that checks for key inputs
        elif event.type == pygame.KEYDOWN:

            #If statement that defines the input as a promotion input
            if promotion_moves:
                promotion_input(event.key)

    minimax_move_maker(board)

    #Executes the draw function
    draw()

#Quits programs
pygame.quit()
sys.exit()