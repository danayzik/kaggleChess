import chess
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

SQUARE_CONTROL_VALUE = 0.1
board = chess.Board()


def evaluate_piece_activity(board):
    scores = {chess.WHITE: 0, chess.BLACK: 0}
    for square, piece in board.piece_map().items():
        piece_value = 0
        color = piece.color
        opponent_color = not color
        controlled_squares = board.attacks(square)
        piece_value += len(controlled_squares) * SQUARE_CONTROL_VALUE
        for defended_square in controlled_squares:
            defender = board.piece_at(defended_square)
            if defender and defender.color == color:
                piece_value += PIECE_VALUES[defender.piece_type] * 0.5
        for attacked_square in controlled_squares:
            attacked = board.piece_at(attacked_square)
            if attacked and attacked.color == opponent_color:
                piece_value += PIECE_VALUES[attacked.piece_type]
        scores[color] += piece_value
    return scores

def evaluate_board():
    pass

def minimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval
