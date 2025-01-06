from players.human_player import HumanPlayer
from players.stockfish_player import StockfishPlayer
from game_sim.game import Game


p1 = HumanPlayer()
p2 = HumanPlayer()
# p2.set_engine_strength(1500)
g = Game(p1, p2, True)
g.run()