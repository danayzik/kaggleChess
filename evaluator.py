from stockfish import Stockfish

class Evaluator:
    def __init__(self):
        stockfish_path = "D:\chess\stockfish\stockfish-windows-x86-64-avx2"
        self.stockfish = Stockfish(stockfish_path)

    def get_eval(self, fen :str) -> float:
        self.stockfish.set_fen_position(fen)
        evaluation = self.stockfish.get_evaluation()
        cp = evaluation['type'] == 'cp'
        if cp:
            value = evaluation['value']
            return value
        mate_moves = evaluation['value']
        value = float('inf') if mate_moves > 0 else float('-inf')
        return value


# e = Evaluator()
# e.stockfish.set_depth(1)
# fen = "3rkb1r/1p2pppp/p1p5/4P3/8/3B2B1/PPP2K1P/4R3 b k - 1 18"
# print(e.get_eval(fen))