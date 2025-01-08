import chess
from players.botv2 import BotV2
from players.human_player import HumanPlayer
from players.player import Player
from players.stockfish_player import StockfishPlayer
from game_sim.game import Game
from players.botv1 import BotV1
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from players.test_bot_api import TestBotApi
import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper
botv1_wins = 0
stockfish_wins = 0
draws = 0
games = 1
counter_lock = Lock()

@time_it
def play_game():
    global botv1_wins, stockfish_wins, draws, games
    p1 = TestBotApi()
    # p1 = BotV2()
    # p2 = BotV1()
    p2 = StockfishPlayer()
    p2.set_engine_strength(1320, 0.1)
    g = Game(p1, p2, False)
    res = g.run()
    # with counter_lock:
    #     if res == 1:
    #         botv1_wins += 1
    #     elif res == 2:
    #         stockfish_wins += 1
    #     elif res == 0:
    #         draws += 1
    #     print(f"Game {games} finished")
    #     games += 1

def run_games_in_threads():
    num_threads = 10
    iterations_per_thread = 10

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(play_game) for _ in range(num_threads * iterations_per_thread)]

    for future in futures:
        future.result()

if __name__ == "__main__":
    play_game()
    # run_games_in_threads()
    # print(f"BotV1 wins: {botv1_wins}")
    # print(f"Stockfish wins: {stockfish_wins}")
    # print(f"Draws: {draws}")



