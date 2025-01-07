from typing import Optional
import chess
from players.bot_v2_constants import *
from players.player import Player

def piece_values(piece_type: int) -> int:
    if piece_type == chess.QUEEN:
        return 9
    elif piece_type == chess.ROOK:
        return 5
    elif piece_type == chess.BISHOP or piece_type == chess.KNIGHT:
        return 3
    elif piece_type == chess.PAWN:
        return 1
    return 0

def is_endgame(board: chess.Board) -> bool:
    material = sum([piece_values(piece.piece_type) for piece in board.piece_map().values()])
    endgame_threshold = 28
    return material <= endgame_threshold

def sorted_legal_moves(board:chess.Board):
    legal_moves = list(board.legal_moves)
    sorted_moves = sorted(
        legal_moves,
        key=lambda move: (
            not board.gives_check(move),
            not board.is_capture(move)
        )
    )
    return sorted_moves

def evaluate_piece(board, square, piece, piece_char):
    phase_index = 1 if is_endgame(board) else 0
    piece_enum = CHAR_TO_PIECE[piece_char]
    piece_value = PIECE_VALUES[piece_enum]
    color = piece.color
    controlled_squares = board.attacks(square)
    color_int = 0 if piece.color == chess.WHITE else 1
    piece_index =  piece.piece_type-1
    row_index = abs(color_int*7 - chess.square_rank(square))
    file_index = chess.square_rank(square)
    piece_value += len(controlled_squares) * SQUARE_CONTROL_VALUE + PHASE_TABLES[phase_index][piece_index][row_index][file_index]
    for square in controlled_squares:
        controlled_piece = board.piece_at(square)
        if controlled_piece:
            controlled_piece_enum = CHAR_TO_PIECE[controlled_piece.symbol()]
            if color == controlled_piece.color:
                piece_value += DEFEND_VALUES[controlled_piece_enum]
            else:
                piece_value += ATTACK_VALUES[controlled_piece_enum]
    return piece_value

def is_draw(board: chess.Board) -> bool:
    return board.is_stalemate() or board.is_fifty_moves() or board.is_repetition() or board.is_fifty_moves()

def evaluate_board(board: chess.Board) -> float:
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')
        else:
            return float('inf')
    if is_draw(board):
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
        scores[piece.color] += value
    evaluation = scores[chess.WHITE] - scores[chess.BLACK]
    return evaluation


def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None
    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        legal_moves = sorted_legal_moves(board)
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval >= max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        legal_moves = sorted_legal_moves(board)
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval <= min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff

        return min_eval, best_move

class BotV2(Player):
    def get_move(self, board: chess.Board) -> chess.Move:
        maximize = self.color == chess.WHITE
        alpha = -float('inf')
        beta = float('inf')
        eval, move = minimax(board, 3, alpha, beta, maximize)
        print(eval)
        return move


    def report_game_over(self, winner: Optional[chess.Color]) -> None:
        if winner is None:
            print("Draw")
        if winner == self.color:
            print("botV2 wins")
        else:
            print("botV2 loses")





