import pygame
import chess

from io import BytesIO
from game_sim.game_visual_constants import HEIGHT, WIDTH, SQUARE_SIZE, IMAGE_DIR, GAME_HEIGHT, GAME_WIDTH


def load_chess_pieces():
    piece_to_image = {}
    colors = ['W', 'B']
    piece_names = ['P', 'K', 'Q', 'R', 'B', 'N']
    for color in colors:
        for piece in piece_names:
            symbol = piece
            if color == 'B':
                symbol = symbol.lower()
            png_path = f"{IMAGE_DIR}\\{color}_{piece}.png"  # Updated to use .png files
            piece_to_image[symbol] = load_png_to_surface(png_path, SQUARE_SIZE)
    return piece_to_image


def load_png_to_surface(png_path, size):
    image = pygame.image.load(png_path).convert_alpha()  # Loads the PNG image
    return pygame.transform.scale(image, (size, size))  # Scales the image to the given size



class GameScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Visualization")
        self.pieces = load_chess_pieces()

    @staticmethod
    def refresh():
        pygame.display.flip()

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


    def show_promotion_ui(self, color: chess.Color):
        if color == chess.WHITE:
            piece_names = ["Q", 'R', 'B', 'N']
        else:
            piece_names = ["q", 'r', 'b', 'n']
        promotion_ui_height = GAME_HEIGHT
        for i, piece_name in enumerate(piece_names):
            piece_image = self.pieces[piece_name]
            pygame.draw.rect(self.screen, (200, 200, 200), (WIDTH - GAME_WIDTH+i * SQUARE_SIZE, promotion_ui_height, SQUARE_SIZE, SQUARE_SIZE))
            self.screen.blit(piece_image,
                        (i * SQUARE_SIZE + (SQUARE_SIZE - piece_image.get_width()) // 2, promotion_ui_height))
        self.refresh()


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
        self.draw_pieces(board)
        self.refresh()