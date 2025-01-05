import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}
CHAR_TO_PIECE = {
    'p': chess.PAWN,
    'P': chess.PAWN,
    'n': chess.KNIGHT,
    'N': chess.KNIGHT,
    'b': chess.BISHOP,
    'B': chess.BISHOP,
    'r': chess.ROOK,
    'R': chess.ROOK,
    'q': chess.QUEEN,
    'Q': chess.QUEEN,
    'k': chess.KING,
    'K': chess.KING
}
ATTACK_VALUES = {
    chess.PAWN: 0.05,
    chess.KNIGHT: 0.2,
    chess.BISHOP: 0.2,
    chess.ROOK: 0.6,
    chess.QUEEN: 1,
    chess.KING: 1.2
}
DEFEND_VALUES = {
    chess.PAWN: 0.25,
    chess.KNIGHT: 0.2,
    chess.BISHOP: 0.2,
    chess.ROOK: 0.1,
    chess.QUEEN: 0.05,
    chess.KING: 0
}
SQUARE_CONTROL_VALUE = 0.05
board = chess.Board()
fianchetto_bonus = 0.08
castle_rights_bonus = 0.5

def precompute_long_diagonals():
    long_diagonals = set()
    for square in chess.SQUARES:
        if chess.square_file(square) == chess.square_rank(square) or \
           chess.square_file(square) + chess.square_rank(square) == 7:
            long_diagonals.add(square)
    return long_diagonals


long_diagonals = precompute_long_diagonals()
def square_value(square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    center_score = round(5 - ((3.5 - file)**2 + (3.5 - rank)**2)**0.5, 2)
    return center_score*0.2


square_value_map = {square: square_value(square) for square in chess.SQUARES}

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

# add game over eval
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
