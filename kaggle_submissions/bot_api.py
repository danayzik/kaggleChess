import os
import subprocess



class BotApi:
    def __init__(self):
        self.bot = self.init_bot()

    def set_color(self, color: str):
        self.send_str(color)


    def get_move(self, enemy_move: str) -> str:
        try:
            self.send_str(enemy_move)
            move = self.read_move()
            return move

        except Exception as e:
            print(e)
            self.bot.kill()



    def init_bot(self):
        base_path = '/kaggle_simulations/agent/'
        bot_path = os.path.join(base_path, 'chessBot')
        subprocess.run(['chmod', '+x', bot_path])
        process = subprocess.Popen(
            bot_path,
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



