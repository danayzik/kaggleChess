from stockfish import Stockfish
import subprocess
class Evaluator:
    def __init__(self, depth: int):
        stockfish_path = "D:\chess\stockfish\stockfish-windows-x86-64-avx2"
        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.set_depth(depth)

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


class StaticStockfishEvaluator:
    def __init__(self, path="D:\chess\stockfish\stockfish-windows-x86-64-avx2"):
        self.engine = subprocess.Popen(
            [path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1
        )
        self._send_command("uci")
        self._wait_for("uciok")
        self._send_command("isready")
        self._wait_for("readyok")

    def _send_command(self, command):
        self.engine.stdin.write(command + "\n")
        self.engine.stdin.flush()

    def _wait_for(self, expected):
        while True:
            line = self.engine.stdout.readline().strip()
            if expected in line:
                break

    def get_eval(self, fen):
        self._send_command(f"position fen {fen}")
        self._send_command("eval")
        while True:

            line = self.engine.stdout.readline().strip()
            if line.startswith("NNUE evaluation"):
                line = self.engine.stdout.readline().strip()
                return float(line.split()[2])*100
            elif line.startswith("Final evaluation:"):
                if "b" in fen:
                    return float('inf')
                else:
                    return float('-inf')

    def quit(self):
        self._send_command("quit")
        self.engine.terminate()

