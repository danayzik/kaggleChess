from typing import Optional

from game_sim.game_screen import GameScreen
from players.player import Player
import random
import chess
import pygame

OPENINGS = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "rnbqkbnr/1p2pp1p/p2p2p1/8/2PNP3/8/PP3PPP/RNBQKB1R w KQkq - 0 6",
    "r1b1kb1r/ppppq1pp/2n2n2/1B2p3/4N3/5N2/PPPPQPPP/R1B1K2R w KQkq - 3 7",
    "rnbqkb1r/p2ppppp/5n2/2pP4/2p5/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 5",
    "rnbqk1nr/p1p1bppp/1p2p3/3pP3/3P4/2N5/PPP2PPP/R1BQKBNR w KQkq - 0 5",
    "r2qk1nr/ppp2pp1/2np3p/2b1p3/2B1P1b1/2PP1N2/PP3PPP/RNBQ1RK1 w kq - 0 7",
    "rn1qk1nr/pp2ppbp/3p2p1/2p5/2PP2b1/2N1PN2/PP3PPP/R1BQKB1R w KQkq c6 0 6",
    "rnbqkbnr/1p2pp1p/p2p2p1/8/2PNP3/8/PP3PPP/RNBQKB1R w KQkq - 0 6",
]


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
        fen = random.choice(OPENINGS)
        # fen = "8/6k1/8/8/8/7r/4K3/8 w - - 0 1"
        self.board.set_fen(fen)
        if visual:
            self.game_screen = GameScreen()
            self.game_screen.update(self.board)
        self.white_player = player1
        self.black_player = player2
        self.colors = [chess.WHITE, chess.BLACK]
        self.assign_colors(player1, player2)
        self.white_player.setup_board(fen)
        self.black_player.setup_board(fen)
        self.running = False
        self.visuals = visual
        self.last_move: Optional[chess.Move] = None



    def assign_colors(self, player1: Player, player2: Player) -> None:
        random.shuffle(self.colors)

        player1.set_color(self.colors[0])
        player2.set_color(self.colors[1])
        if chess.WHITE == self.colors[0]:
            self.white_player = player1
            self.black_player = player2
            print("player1 is white, player2 is black")
        else:
            self.black_player = player1
            self.white_player = player2
            print("player1 is black, player2 is white")

    def run(self) -> int:
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
            self.report_result()
            self.game_screen.display_game_over_message(self.board)
        self.running = False
        return self.report_result()


    def fetch_play_update(self, player: Player, human, visual) -> bool:
        if human:
            return self.handle_human_move(player)
        move = player.get_move(self.last_move)
        self.board.push(move)
        self.last_move = move
        if visual:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.report_result()
                    pygame.quit()
                    exit(0)
            self.game_screen.update(self.board)
        return self.board.is_game_over(claim_draw=True)

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
                self.last_move = potential_move
                self.game_screen.update(self.board)
                return self.board.is_game_over(claim_draw=True)
            self.game_screen.update(self.board)

    def report_result(self) -> int:
        result = self.board.result()
        if result == "1-0":
            winner = chess.WHITE

        elif result == "0-1":
            winner = chess.BLACK
        else:
            winner = None
        if winner is None:
            ret = 0
        elif winner == self.colors[0]:
            ret = 1
        else:
            ret = 2
        self.white_player.report_game_over(winner)
        self.black_player.report_game_over(winner)
        return ret


