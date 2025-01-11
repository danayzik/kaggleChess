from bot_api import BotApi
import os
import sys

start = True
bot = BotApi()
def chess_bot(obs):
    global start
    last_move = obs.lastMove
    if start:
        from Chessnut import Game
        game = Game(obs.board)
        color = game.state.player
        bot.set_color(color)
        fen = game.get_fen()
        bot.setup_board(fen)
        start = False
        move = bot.get_move("start")
        return move
    move = bot.get_move(last_move)
    return move