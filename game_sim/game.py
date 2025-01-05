import pygame
from game_screen import GameScreen
from players.player import Player
import random
import chess


class Game:
    def __init__(self, player1: Player, player2: Player, visual=False):
        if visual:
            pygame.init()
            self.game_screen = GameScreen()
        self.white_player = player1
        self.black_player = player2
        self.assign_colors(player1, player2)
        self.running = False
        self.board = chess.Board()
        self.visuals = visual


    def assign_colors(self, player1: Player, player2: Player) -> None:
        colors = [chess.WHITE, chess.BLACK]
        random.shuffle(colors)
        player1.set_color(colors[0])
        player2.set_color(colors[1])
        if chess.WHITE == colors[0]:
            self.white_player = player1
            self.black_player = player2
        else:
            self.black_player = player1
            self.white_player = player2

    def run(self):
        self.running = True
        self.game_screen.draw_pieces(self.board)
        while self.running:
            game_over = self.fetch_play_update(self.white_player, True)
            if game_over:
                break
            game_over = self.fetch_play_update(self.black_player, True)
            if game_over:
                break
        if self.visuals:
            self.game_screen.display_game_over_message(self.board)
        self.running = False



    def fetch_play_update(self, player: Player, visual=False) -> bool:
        move = player.get_move(self.board)
        self.board.push(move)
        if visual:
            self.game_screen.update(self.board)
        return self.board.is_game_over()
