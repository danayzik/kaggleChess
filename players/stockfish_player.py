from pygame import Surface
import chess.engine
from players.player import Player
import chess
from typing import Optional

class StockfishPlayer(Player):


    def __init__(self):
        super().__init__()
        stockfish_path = "D:\chess\stockfish\stockfish-windows-x86-64-avx2"
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.time_limit = 2.0

    def set_engine_strength(self, elo: int, time_limit=2.0):
        self.engine.configure({"UCI_LimitStrength": True, "UCI_Elo": elo})
        self.time_limit = time_limit

    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        self.engine.quit()
        if winner is None:
            print("Draw")
        if winner == self.color:
            print("stockfish wins")
        else:
            print("stockfish loses")




    def get_move(self, board: chess.Board) -> chess.Move:
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit))
        return result.move





