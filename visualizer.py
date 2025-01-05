import pygame
import chess
import cairosvg
from io import BytesIO
from bot import minimax

pygame.init()
WIDTH, HEIGHT = 512, 576
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Visualization")

def load_svg_to_surface(svg_path, size):
    png_data = BytesIO(cairosvg.svg2png(url=svg_path, output_width=size, output_height=size))
    image = pygame.image.load(png_data, "PNG")
    return pygame.transform.scale(image, (size, size))

def display_game_over_message(board):
    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()
    font = pygame.font.Font(None, 48)

    # Check for game over conditions
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            message = "Black Wins (Checkmate)"
        else:
            message = "White Wins (Checkmate)"
    elif board.is_stalemate():
        message = "Stalemate (Draw)"
    elif board.is_insufficient_material():
        message = "Insufficient Material (Draw)"
    elif board.is_fivefold_repetition():
        message = "Fivefold Repetition (Draw)"
    else:
        message = "Game Over (Draw)"
    text_surface = font.render(message, True, (255, 0, 0))  # Red color
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Wait for the user to quit the game after displaying the message
    waiting_for_quit = True
    while waiting_for_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def load_chess_pieces():
    piece_to_image = {}
    colors = ['W', 'B']
    piece_names = ['P', 'K','Q', 'R', 'B', 'N']
    for color in colors:
        for piece in piece_names:
            symbol = piece
            if color == 'B':
                symbol = symbol.lower()
            svg_path = f"assets\\pieces\\{color}_{piece}.svg"
            piece_to_image[symbol] = load_svg_to_surface(svg_path, SQUARE_SIZE)
    return piece_to_image


def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT-64, SQUARE_SIZE*4, 64))
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board, pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            screen.blit(pieces[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

def highlight_square(square):
    if square is not None:
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        pygame.draw.rect(screen, pygame.Color("yellow"), pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

# fen = "8/1P1k2K1/8/8/8/8/8/8 b - - 1 0"
# board = chess.Board(fen)
board = chess.Board()
pieces = load_chess_pieces()
selected_square = None
legal_moves = []

def show_promotion_ui():
    # Create a small UI for promotion selection
    # Display options for Black Queen, Rook, Bishop, Knight outside the normal game window
    promotion_pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    piece_names = ["q", 'r', 'b', 'n']
    screen_width, screen_height = pygame.display.get_surface().get_size()
    option_width = SQUARE_SIZE
    promotion_ui_height = screen_height - 64  # Make the promotion UI appear below the board
    # Draw promotion options outside the main board window
    for i, piece_name in enumerate(piece_names):
        piece_image = pieces[piece_name]  # Load black pieces (bQ, bR, bB, bN)
        pygame.draw.rect(screen, (200, 200, 200), (i * option_width, promotion_ui_height, option_width, 64))
        screen.blit(piece_image, (i * option_width + (option_width - piece_image.get_width()) // 2, promotion_ui_height))
    pygame.display.flip()

    # Handle mouse click to select promotion piece
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if promotion_ui_height <= y <= screen_height:  # Check if click is within the promotion UI area
                    index = x // option_width
                    if 0 <= index < len(promotion_pieces):
                        return promotion_pieces[index]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_square = get_square_under_mouse(event.pos)
            if selected_square is None:
                piece = board.piece_at(clicked_square)
                if piece and (piece.color == board.turn):
                    selected_square = clicked_square
                    legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
            else:
                move = chess.Move(from_square=selected_square, to_square=clicked_square)
                if board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(clicked_square) in [0,7]:
                    promotion_piece = show_promotion_ui()
                    move = chess.Move(from_square=selected_square, to_square=clicked_square, promotion=promotion_piece)

                if move in legal_moves:

                    board.push(move)
                selected_square = None
                legal_moves = []

    if board.turn == chess.WHITE:
        # Call minimax to get the best move for the bot (white)
        eval_score, best_move = minimax(board, 3, float('-inf'), float('inf'), True)
        print(eval_score)
        board.push(best_move)

    draw_board()
    if selected_square is not None:
        highlight_square(selected_square)
        for move in legal_moves:
            highlight_square(move.to_square)

    draw_pieces(board, pieces)
    pygame.display.flip()
    if board.is_game_over():
        display_game_over_message(board)
        break  # Exit the game loop after displaying the result

pygame.quit()
