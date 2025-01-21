from typing import Optional
import chess

from players.player import Player
import subprocess
import time

move_count = 1
total_time = 0.0

def time_it(func):

    def wrapper(*args, **kwargs):
        global move_count
        global total_time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        move_count += 1
        total_time += (end_time - start_time)
        return result
    return wrapper

class TestBotApi(Player):
    def __init__(self):
        super().__init__()
        self.bot = self.init_bot()

    def set_color(self, color: chess.Color):
        global move_count, total_time
        move_count = 1
        total_time = 0.0
        super().set_color(color)
        symbol = 'w' if color else 'b'
        self.send_str(symbol)


    @time_it
    def get_move(self, enemy_move: chess.Move) -> chess.Move:
        try:
            if enemy_move is None:
                message = "start"
            else:
                message = chess.Move.uci(enemy_move)

            self.send_str(message)
            move_uci = self.read_move()
            move = chess.Move.from_uci(move_uci)
            return move

        except Exception as e:
            self.bot.kill()


    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Average time: {total_time/move_count:.6f} seconds")
        self.send_str("end")
        self.bot.kill()


    def init_bot(self):
        process = subprocess.Popen(
            "C:\\Users\\danay\\PycharmProjects\\kaggleChess\\players\\chessBot.exe",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process

    def send_str(self, input_str: str):

        self.bot.stdin.write(input_str + "\n")
        self.bot.stdin.flush()

    def read_move(self):
        output = self.bot.stdout.readline()
        return output.strip()

    def setup_board(self, fen: str) -> None:

        self.send_str(fen)



