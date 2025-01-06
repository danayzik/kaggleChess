from players.human_player import HumanPlayer
from players.stockfish_player import StockfishPlayer
from game_sim.game import Game
from players.botv1 import BotV1


p1 = BotV1()
p2 = BotV1()
# p2 = StockfishPlayer()
# p2.set_engine_strength(1320,0.5)
g = Game(p1, p2, True)
g.run()