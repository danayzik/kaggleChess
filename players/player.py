from abc import ABC, abstractmethod
import chess
from typing import Optional
from pygame import Surface


class Player(ABC):
    def __init__(self):
        self.color: Optional[chess.Color] = None

    @abstractmethod
    def get_move(self, board: chess.Board) -> chess.Move:
        pass



    @abstractmethod
    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        pass



    @abstractmethod
    def get_clicked_square(self, board: chess.Board, screen: Surface) -> chess.Piece:
        pass


    def set_color(self, color: chess.Color):
        self.color = color