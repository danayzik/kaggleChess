import pygame
import chess
import cairosvg
from io import BytesIO
from game_visual_constants import HEIGHT, WIDTH, SQUARE_SIZE, IMAGE_DIR


def load_chess_pieces():
    piece_to_image = {}
    colors = ['W', 'B']
    piece_names = ['P', 'K','Q', 'R', 'B', 'N']
    for color in colors:
        for piece in piece_names:
            symbol = piece
            if color == 'B':
                symbol = symbol.lower()
            svg_path = f"{IMAGE_DIR}\\{color}_{piece}.svg"
            piece_to_image[symbol] = load_svg_to_surface(svg_path, SQUARE_SIZE)
    return piece_to_image


def load_svg_to_surface(svg_path, size):
    png_data = BytesIO(cairosvg.svg2png(url=svg_path, output_width=size, output_height=size))
    image = pygame.image.load(png_data, "PNG")
    return pygame.transform.scale(image, (size, size))


class GameScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Visualization")
        self.pieces = load_chess_pieces()
        self.draw_board()


    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        pygame.draw.rect(self.screen, (0, 0, 0), (0, HEIGHT - 64, SQUARE_SIZE * 4, 64))
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, board):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                self.screen.blit(self.pieces[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def highlight_square(self, square):
        if square is not None:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            pygame.draw.rect(self.screen, pygame.Color("yellow"),
                             pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    #Make this player dependant
    def show_promotion_ui(self):
        # Create a small UI for promotion selection
        # Display options for Black Queen, Rook, Bishop, Knight outside the normal game window
        promotion_pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        piece_names = ["q", 'r', 'b', 'n']
        screen_width, screen_height = pygame.display.get_surface().get_size()
        option_width = SQUARE_SIZE
        promotion_ui_height = screen_height - 64  # Make the promotion UI appear below the board
        # Draw promotion options outside the main board window
        for i, piece_name in enumerate(piece_names):
            piece_image = self.pieces[piece_name]  # Load black pieces (bQ, bR, bB, bN)
            pygame.draw.rect(self.screen, (200, 200, 200), (i * option_width, promotion_ui_height, option_width, 64))
            self.screen.blit(piece_image,
                        (i * option_width + (option_width - piece_image.get_width()) // 2, promotion_ui_height))
        pygame.display.flip()
        # Move to player class
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

    # move waiting for quit to game/player
    def display_game_over_message(self, board):
        font = pygame.font.Font(None, 48)
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
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        # Wait for the user to quit the game after displaying the message
        waiting_for_quit = True
        while waiting_for_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


    def update(self, board: chess.Board):
        self.draw_board()
        self.draw_pieces()