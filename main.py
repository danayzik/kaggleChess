import pygame
import chess
import cairosvg
from io import BytesIO


# Initialize pygame
pygame.init()
# Screen dimensions
WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Visualization")

# Function to convert SVG to a pygame surface
def load_svg_to_surface(svg_path, size):
    # Convert SVG to PNG bytes
    png_data = BytesIO(cairosvg.svg2png(url=svg_path, output_width=size, output_height=size))
    # Load PNG into a pygame surface
    image = pygame.image.load(png_data, "PNG")
    return pygame.transform.scale(image, (size, size))

# Load chess piece images
def load_chess_pieces():
    pieces = {}
    piece_names = ["white_knight"]
    for piece in piece_names:
        svg_path = f"assets/pieces/{piece}.svg"  # Path to your SVGs
        pieces[piece] = load_svg_to_surface(svg_path, SQUARE_SIZE)
    return pieces

# Draw the chessboard
def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(board, pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            screen.blit(pieces[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Main game loop
board = chess.Board()
pieces = load_chess_pieces()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_board()
    draw_pieces(board, pieces)
    pygame.display.flip()

pygame.quit()
