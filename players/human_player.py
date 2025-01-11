import chess
import pygame


from game_sim.game_visual_constants import SQUARE_SIZE, HEIGHT, GAME_HEIGHT
from players.player import Player
from typing import Optional

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)




class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_move(self, move: chess.Move) -> chess.Move:
        pass

    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        if winner is None:
            print("drew")
        elif winner == self.color:
            print("I won")
        else:
            print("I lost")

    def get_clicked_piece(self, board: chess.Board, screen: pygame.Surface) -> tuple[chess.Piece, chess.Square]:
        owned_piece = False
        square = None
        piece = None
        while not owned_piece:
            square = self.get_clicked_square(board, screen)
            piece = board.piece_at(square)
            if piece is not None and isinstance(piece, chess.Piece):
                owned_piece = piece.color == self.color
        return piece, square

    def is_human(self):
        return True


    def get_clicked_square(self, board: chess.Board, screen: pygame.Surface) -> chess.Square:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)  # engine still running
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_square = get_square_under_mouse(event.pos)
                    return clicked_square

    def get_clicked_promotion_piece(self) -> chess.Piece:
        promotion_pieces = [chess.Piece(piece_type, self.color) for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if HEIGHT - GAME_HEIGHT <= y <= HEIGHT:
                        index = x // SQUARE_SIZE
                        if 0 <= index < len(promotion_pieces):
                            return promotion_pieces[index]




