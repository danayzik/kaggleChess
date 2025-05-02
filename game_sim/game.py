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
    "r1bqkb1r/pp1ppppp/2n2n2/8/2P5/8/PP1QPPPP/RNB1KBNR w KQkq - 3 5",
    "rnbqk2r/ppp1ppbp/5np1/3p2B1/3P4/2P5/PP1NPPPP/R2QKBNR w KQkq - 0 5",
    "rnbqkb1r/pp2pppp/5n2/3p4/8/3P2P1/PP2PP1P/RNBQKBNR w KQkq - 1 5",
    "rnbq1rk1/ppppppbp/5np1/8/8/1P2PN2/PBPP1PPP/RN1QKB1R w KQ - 1 5",
    "rn1qkb1r/pp2pppp/2p2n2/3p4/2PP2b1/4PN2/PP3PPP/RNBQKB1R w KQkq - 0 5",
    "r1bqkb1r/pppnnppp/3pp3/8/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 2 5",
    "rnq1kb1r/ppp1pppp/5n2/3p1b2/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 3 5",
    "rnbqk1nr/ppp2pbp/3pp1p1/8/8/5NP1/PPPPPPBP/RNBQ1RK1 w kq - 0 5",
    "rnbqk2r/p1ppppbp/1p3np1/8/8/5NP1/PPPPPPBP/RNBQ1RK1 w kq - 0 5",
    "r1bqkbnr/pp1p1ppp/2n1p3/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5",
    "rnbqkb1r/ppp3pp/4pn2/3p1p2/8/PP2P3/1BPP1PPP/RN1QKBNR w KQkq - 1 5",
    "rnbqk2r/pp1pppbp/6pn/2p5/3PP3/2N5/PPP2PPP/R2QKBNR w KQkq - 0 5",
    "rnbqkbnr/pp4pp/8/2pppp2/8/4PPK1/PPPP2PP/RNBQ1BNR w kq - 0 5",
    "rnbqkb1r/p2ppppp/5n2/2p5/8/5NP1/PPP1PP1P/RNBQKB1R w KQkq - 0 5",
    "rnbqk2r/ppp1ppbp/3p1np1/8/8/1P2PN2/PBPP1PPP/RN1QKB1R w KQkq - 0 5",
    "rnbqk2r/ppp1bppp/4pn2/3p4/2PP4/4PN2/PP3PPP/RNBQKB1R w KQkq - 3 5",
    "rnbqkb1r/ppp2ppp/3p4/8/4n3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 5",
    "rnbqk2r/ppp1ppbp/3p1np1/8/3P1B2/4PN2/PPP2PPP/RN1QKB1R w KQkq - 2 5",
    "rnbqkb1r/ppp2p1p/3p1pp1/8/8/1P3N2/P1PPPPPP/RN1QKB1R w KQkq - 0 5",
    "rn1qkb1r/pbpp1ppp/4pn2/1p6/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 2 5",
    "rnbqk2r/ppppb1pp/4pn2/5p2/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 3 5",
    "rnbqk2r/ppp1ppbp/3p1np1/6B1/3P4/2N2N2/PPP1PPPP/R2QKB1R w KQkq - 0 5",
    "rnbqkb1r/ppp2ppp/5n2/3p4/3P4/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 5",
    "rn1qkb1r/pb1ppppp/1p3n2/2pP4/4P3/2P5/PP3PPP/RNBQKBNR w KQkq - 1 5",
    "r1bqkb1r/pppn1ppp/3p1n2/4p3/4P3/2N3P1/PPPP1PBP/R1BQK1NR w KQkq - 2 5",
    "rnbqk2r/ppppnpbp/4p1p1/8/3P4/2P3P1/PP2PPBP/RNBQK1NR w KQkq - 1 5",
    "r1bqkb1r/ppp2ppp/2n2n2/3pp3/8/3P1NP1/PPP1PPBP/RNBQK2R w KQkq - 1 5",
    "r1bqkb1r/ppp2ppp/2n2n2/3pp3/2P5/1P2P3/PB1P1PPP/RN1QKBNR w KQkq - 0 5",
    "r1bqkb1r/pp1npppp/2p2n2/3p4/5P2/4PN2/PPPPB1PP/RNBQK2R w KQkq - 2 5",
    "rnbqkb1r/pp2pp1p/2p2np1/3p4/8/5NP1/PPPPPPBP/RNBQ1K1R w kq - 0 5",
    "rnbqk2r/ppp1ppbp/5np1/3p4/3P4/4PN2/PPP1BPPP/RNBQK2R w KQkq - 2 5",
    "r3kbnr/pppqpppp/2n5/3p1b2/8/3P1NP1/PPP1PPBP/RNBQK2R w KQkq - 1 5",
    "rnbqkb1r/ppp2p1p/5pp1/3p4/3P4/4P3/PPP2PPP/RN1QKBNR w KQkq - 0 5",
    "rnbqk2r/ppp1ppbp/3p1np1/8/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq - 2 5",
    "r1bqkb1r/pppp1ppp/2n2n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5",
    "rnbqkb1r/ppp1pppp/8/8/4P3/2n5/PP1P1PPP/R1BQKBNR w KQkq - 0 5",
    "r1bqkbnr/pp1ppp1p/2n3p1/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5",
    "r2qkbnr/1bpppppp/ppn5/8/2P5/5NP1/PP1PPPBP/RNBQK2R w KQkq - 1 5",
    "r1bqkb1r/pp2pppp/2n2n2/2pp4/8/1P2PN2/PBPP1PPP/RN1QKB1R w KQkq - 1 5",
    "rnbqkb1r/pp3ppp/3ppn2/2p5/2B1P3/2PP4/PP3PPP/RNBQK1NR w KQkq - 0 5",
    "rnbqk1nr/pp1pppbp/6p1/8/3P4/2P5/PP3PPP/RNBQKBNR w KQkq - 1 5",
    "rnbqk2r/ppp2ppp/3bpn2/3p4/3P1B2/5N2/PPPQPPPP/RN2KB1R w KQkq - 2 5",
    "r1bqk2r/ppppbppp/2n2n2/4p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 6 5",
    "r1bqkbnr/ppp3pp/2n2p2/3pp3/3P4/1P3N2/PBP1PPPP/RN1QKB1R w KQkq - 0 5",
    "r1b1kbnr/ppqnpppp/2pp4/8/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 3 5",
    "r1bqkbnr/pppp1ppp/6n1/3Pp3/4P3/5N2/PPP2PPP/RNBQKB1R w KQkq - 3 5",
    "r1bqkb1r/pppnppp1/5n1p/3p2B1/3P4/2N2N2/PPP1PPPP/R2QKB1R w KQkq - 0 5",
    "r1bqk1nr/pp1pppbp/2n3p1/2p5/8/5NP1/PPPPPPBP/RNBQ1RK1 w kq - 4 5",
    "rnbqk2r/ppppppbp/6p1/7n/3P4/2N5/PPP1PPP1/R1BQKBNR w KQkq - 0 5",
    "rnbqkbnr/pp3pp1/4p2p/2ppP3/3P4/2N5/PPP2PPP/R1BQKBNR w KQkq - 0 5",
    "rnbqkbnr/p4ppp/2p1p3/1p1p4/8/5NP1/PPPPPPBP/RNBQ1RK1 w kq - 0 5",
    "rnbqkbnr/pp2ppp1/2p5/3P4/3P3p/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 5",
    "r1bqkbnr/pp1n1ppp/2pp4/4p3/3PP3/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 0 5",
    "rnbqkb1r/pppppppp/8/2PnP3/8/8/PP1P1PPP/RNBQKBNR w KQkq - 1 5",
    "rnbqk2r/ppp1ppbp/3p1np1/8/1P6/P4N2/1BPPPPPP/RN1QKB1R w KQkq - 2 5",
    "rn1qkb1r/pbpp1ppp/1p2pn2/8/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 2 5",
    "rn1qkb1r/pbpp1ppp/1p2pn2/8/3P4/3BPN2/PPP2PPP/RNBQK2R w KQkq - 2 5",
    "rnbqk2r/ppppp1bp/5np1/5p2/3P4/5NP1/PPP1PPBP/RNBQK2R w KQkq - 2 5",
    "rnbqk2r/ppp1bppp/4pn2/3p4/2P5/5NP1/PP1PPPBP/RNBQK2R w KQkq - 4 5",
    "rnbqkbnr/pp3ppp/4p3/2p5/2PpN3/5N2/PP1PPPPP/R1BQKB1R w KQkq - 0 5",
    "r1bqk1nr/pp1pppbp/2n3p1/2p5/8/4PNP1/PPPP1PBP/RNBQK2R w KQkq - 2 5",
    "r1bqkbnr/pppp1ppp/8/8/3np3/1P6/PBPPPPPP/RN1QKB1R w KQkq - 0 5",
    "r1b1k1nr/ppppqppp/2n5/4p3/1b6/1P1P4/PBPNPPPP/R2QKBNR w KQkq - 3 5",
    "rnbqkb1r/pp3ppp/4pn2/2pp4/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq - 0 5",
    "rnbq1rk1/ppppppbp/5np1/8/2P5/1P3N2/PB1PPPPP/RN1QKB1R w KQ - 3 5",
    "rnbqkbnr/pp3ppp/3p4/4p3/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5",
    "rn1qkbnr/1bpp1ppp/pp2p3/8/3PP3/3B4/PPP1NPPP/RNBQK2R w KQkq - 0 5",
    "rnbqkb1r/p2ppp1p/5np1/1ppP4/2P5/6P1/PP2PP1P/RNBQKBNR w KQkq - 0 5",
    "rnbqkb1r/ppp1pppp/5n2/8/3PP3/8/PP3PPP/RNBQKBNR w KQkq - 1 5",
    "rnbqkbnr/p4ppp/1pp1p3/3p4/8/4P1P1/PPPPNPBP/RNBQK2R w KQkq - 0 5",
    "r1bqkb1r/pppp1ppp/2n5/1B2p3/4n3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 0 5",
    "r1bqk1nr/pp1pppbp/2n3p1/2p5/2P5/5NP1/PP1PPPBP/RNBQK2R w KQkq - 4 5",
    "rnbqk2r/ppp1ppbp/5np1/3p4/3P4/3BPN2/PPP2PPP/RNBQK2R w KQkq - 2 5",
    "rnbqkb1r/ppp2ppp/5n2/4p3/4P3/5N2/PPPP2PP/RNBQKB1R w KQkq - 1 5",
    "rnbqkb1r/pp2pppp/5n2/3p4/3P4/5N2/PPP2PPP/RNBQKB1R w KQkq - 1 5",
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
        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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

    def is_game_over(self) -> bool:
        return self.board.is_game_over() or self.board.can_claim_fifty_moves() or self.board.is_repetition()

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
        return self.is_game_over()

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
                return self.is_game_over()
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


