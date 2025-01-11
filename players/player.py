from abc import ABC, abstractmethod
import chess
from typing import Optional
from pygame import Surface


class Player(ABC):
    def __init__(self):
        self.color: Optional[chess.Color] = None
        self.board: Optional[chess.Board] = None

    @abstractmethod
    def get_move(self, move: chess.Move) -> chess.Move:
        pass


    @abstractmethod
    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        pass


    def setup_board(self, fen: str) -> None:
        self.board = chess.Board(fen)


    def get_clicked_piece(self, board: chess.Board, screen: Surface) -> tuple[chess.Piece, chess.Square]:
        pass


    def set_color(self, color: chess.Color):
        self.color = color

    def is_human(self):
        return False


    def get_clicked_square(self, board: chess.Board, screen: Surface) -> chess.Square:
        pass


    def get_clicked_promotion_piece(self) -> chess.Piece:
        pass