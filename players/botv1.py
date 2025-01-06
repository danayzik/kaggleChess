from typing import Optional

import chess
from pygame import Surface
from players.bot_v1_constants import *
from players.player import Player

def evaluate_piece(board, square, piece, piece_char):
    piece_enum = CHAR_TO_PIECE[piece_char]
    piece_value = PIECE_VALUES[piece_enum]
    color = piece.color
    controlled_squares = board.attacks(square)
    if piece_enum == chess.KING:
        piece_value += (1/square_value_map[square])/15
    else:
        piece_value += len(controlled_squares) * SQUARE_CONTROL_VALUE + square_value_map[square]
    for square in controlled_squares:
        controlled_piece = board.piece_at(square)
        if controlled_piece:
            controlled_piece_enum = CHAR_TO_PIECE[controlled_piece.symbol()]
            if color == controlled_piece.color:
                piece_value += DEFEND_VALUES[controlled_piece_enum]
            else:
                piece_value += ATTACK_VALUES[controlled_piece_enum]
    return piece_value


def evaluate_board(board) -> float:
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')  # White loses, assign a very negative score
        else:
            return float('inf')  # Black loses, assign a very positive score
    elif board.is_stalemate():
        return 0
    scores = {chess.WHITE: 0, chess.BLACK: 0}
    white_can_castle = board.has_castling_rights(chess.WHITE)
    black_can_castle = board.has_castling_rights(chess.BLACK)
    white_bonus = castle_rights_bonus if white_can_castle else 0
    black_bonus = castle_rights_bonus if black_can_castle else 0
    scores[chess.WHITE] += white_bonus
    scores[chess.BLACK] += black_bonus
    for square, piece in board.piece_map().items():
        value = evaluate_piece(board, square, piece, piece.symbol())
        if CHAR_TO_PIECE[piece.symbol()] == chess.BISHOP:
            if square in long_diagonals:
                value += fianchetto_bonus
        scores[piece.color] += value
    evaluation = scores[chess.WHITE] - scores[chess.BLACK]
    return evaluation


def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None
    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff

        return min_eval, best_move

class BotV1(Player):
    def get_move(self, board: chess.Board) -> chess.Move:
        maximize = self.color == chess.WHITE
        alpha = -float('inf')
        beta = float('inf')
        eval, move = minimax(board, 3, alpha, beta, maximize)
        return move


    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        pass

    def get_clicked_square(self, board: chess.Board, screen: Surface) -> chess.Piece:
        pass



