import chess
from players.human_player import HumanPlayer
from players.player import Player
from players.stockfish_player import StockfishPlayer
from game_sim.game import Game
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

bot_wins = 0
stockfish_wins = 0
draws = 0
games = 1
counter_lock = Lock()

@time_it
def human_vs_bot():
    global bot_wins, stockfish_wins, draws, games
    p1 = TestBotApi()
    p2 = HumanPlayer()
    g = Game(p1, p2, True)
    try:
        res = g.run()
    except Exception:
        print("Crashed")
        print(g.board.fen())

def run_bot_vs_stockfish(stockfish_path: str, stock_fish_strength = 2000, num_threads: int = 5, iterations_per_thread: int = 10):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(
            bot_vs_stockfish,
            stockfish_path,
            stock_fish_strength, False) for _ in range(num_threads * iterations_per_thread)]

    for future in futures:
        future.result()
    print(f"Bot wins: {bot_wins}")
    print(f"Stockfish wins: {stockfish_wins}")
    print(f"Draws: {draws}")


@time_it
def bot_vs_stockfish(stockfish_path: str, stock_fish_strength = 2000, visuals = False):
    global bot_wins, stockfish_wins, draws, games
    p1 = TestBotApi()
    p2 = StockfishPlayer(stockfish_path)
    p2.set_engine_strength(stock_fish_strength, 0.10)
    g = Game(p1, p2, visuals)
    try:
        res = g.run()
    except Exception as e:
        print(e)
        print("Crashed")
        print(g.board.fen())
        return
    with counter_lock:
        if res == 1:
            bot_wins += 1
        elif res == 2:
            stockfish_wins += 1
        elif res == 0:
            draws += 1
        print(f"Game {games} finished")
        games += 1




