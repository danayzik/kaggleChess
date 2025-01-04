import pygame
import chess
import cairosvg
from io import BytesIO
from bot import minimax

pygame.init()
WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Visualization")

def load_svg_to_surface(svg_path, size):
    png_data = BytesIO(cairosvg.svg2png(url=svg_path, output_width=size, output_height=size))
    image = pygame.image.load(png_data, "PNG")
    return pygame.transform.scale(image, (size, size))

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

board = chess.Board()
pieces = load_chess_pieces()
selected_square = None
legal_moves = []

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
                if move in legal_moves:
                    board.push(move)
                selected_square = None
                legal_moves = []
    if board.turn == chess.WHITE:
        # Call minimax to get the best move for the bot (white)
        eval_score, best_move = minimax(board, 3, True)  # You can adjust the depth
        print(eval_score)
        board.push(best_move)
    draw_board()
    if selected_square is not None:
        highlight_square(selected_square)
        for move in legal_moves:
            highlight_square(move.to_square)

    draw_pieces(board, pieces)
    pygame.display.flip()

pygame.quit()
