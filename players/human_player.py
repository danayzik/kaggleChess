import chess
import pygame
from player import Player
from typing import Optional

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_move(self, board: chess.Board) -> chess.Move:
        pass

    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        if winner is None:
            print("drew")
        if winner == self.color:
            print("I won")
        else:
            print("I lost")

    def get_clicked_square(self, board: chess.Board, screen: pygame.Surface) -> chess.Piece:
        pass



