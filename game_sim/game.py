
from game_sim.game_screen import GameScreen

from players.player import Player
import random
import chess



def is_promotion(piece: chess.Piece, color: chess.Color, to_square: chess.Square) -> bool:
    if piece.piece_type == chess.PAWN:
        if color == chess.WHITE and chess.square_rank(to_square) == 7:
            return True
        elif color == chess.BLACK and chess.square_rank(to_square) == 0:
            return True
    return False

class Game:
    def __init__(self, player1: Player, player2: Player, visual=False):
        self.board = chess.Board()
        if visual:
            self.game_screen = GameScreen()
            self.game_screen.update(self.board)
        self.white_player = player1
        self.black_player = player2
        self.assign_colors(player1, player2)
        self.running = False

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
        if self.visuals:
            self.game_screen.draw_pieces(self.board)
        white_human = self.white_player.is_human()
        black_human = self.black_player.is_human()
        visual = self.visuals or white_human or black_human
        while self.running:
            game_over = self.fetch_play_update(self.white_player, white_human, visual)
            if game_over:
                break
            game_over = self.fetch_play_update(self.black_player, black_human, visual)
            if game_over:
                self.running = False
        if self.visuals:
            self.game_screen.display_game_over_message(self.board)
        self.running = False



    def fetch_play_update(self, player: Player, human, visual) -> bool:
        if human:
            return self.handle_human_move(player)
        move = player.get_move(self.board)
        self.board.push(move)
        if visual:
            self.game_screen.update(self.board)
        return self.board.is_game_over()

    def handle_human_move(self, player: Player) -> bool:
        is_move = False
        while not is_move:
            selected_piece, selected_square = player.get_clicked_piece(self.board, self.game_screen.screen)
            legal_moves = [move for move in self.board.legal_moves if move.from_square == selected_square]
            self.game_screen.highlight_square(selected_square)
            for move in legal_moves:
                self.game_screen.highlight_square(move.to_square)
            self.game_screen.refresh()
            to_square = player.get_clicked_square(self.board, self.game_screen.screen)
            if is_promotion(selected_piece, player.color, to_square):
                self.game_screen.show_promotion_ui(player.color)
                promotion_piece = player.get_clicked_promotion_piece()
                potential_move = chess.Move(selected_square, to_square, promotion=promotion_piece.piece_type)
            else:
                potential_move = chess.Move(selected_square, to_square)
            is_move = self.board.is_legal(potential_move)
            if is_move:
                self.board.push(potential_move)
                self.game_screen.update(self.board)
                return self.board.is_game_over()
            self.game_screen.update(self.board)

