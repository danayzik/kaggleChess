from players.bot import square_value
import chess

def print_square_values():
    values_2d = [[0 for _ in range(8)] for _ in range(8)]
    for square in chess.SQUARES:
        rank = 7 - chess.square_rank(square)
        file = chess.square_file(square)
        values_2d[rank][file] = square_value(square)
    for row in values_2d:
        print(row)
print_square_values()