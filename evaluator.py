from stockfish import Stockfish
import chess

class Evaluator:
    def __init__(self):
        stockfish_path = "D:\chess\stockfish\stockfish-windows-x86-64-avx2"
        self.stockfish = Stockfish(stockfish_path)

    def get_eval(self, board: chess.Board) -> float:
        self.stockfish.set_fen_position(board.fen())
        evaluation = self.stockfish.get_evaluation()
        cp = evaluation['type'] == 'cp'
        if cp:
            value = evaluation['value']/100
            return value
        mate_moves = evaluation['value']
        value = float('inf') if mate_moves > 0 else float('-inf')
        return value