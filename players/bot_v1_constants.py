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