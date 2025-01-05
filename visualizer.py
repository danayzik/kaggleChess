import pygame
import chess
from players.bot import minimax







def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)


# fen = "8/1P1k2K1/8/8/8/8/8/8 b - - 1 0"
# board = chess.Board(fen)
board = chess.Board()

selected_square = None
legal_moves = []





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_square = get_square_under_mouse(event.pos)
            if selected_square is None:
                piece = board.piece_at(clicked_square)
                if piece and (piece.color == board.turn):
                    selected_square = clicked_square
                    legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
            else:
                move = chess.Move(from_square=selected_square, to_square=clicked_square)
                if board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(clicked_square) in [0,7]:
                    promotion_piece = show_promotion_ui()
                    move = chess.Move(from_square=selected_square, to_square=clicked_square, promotion=promotion_piece)

                if move in legal_moves:

                    board.push(move)
                selected_square = None
                legal_moves = []

    if board.turn == chess.WHITE:
        # Call minimax to get the best move for the bot (white)
        eval_score, best_move = minimax(board, 3, float('-inf'), float('inf'), True)
        print(eval_score)
        board.push(best_move)

    draw_board()
    if selected_square is not None:
        highlight_square(selected_square)
        for move in legal_moves:
            highlight_square(move.to_square)

    draw_pieces(board, pieces)
    pygame.display.flip()
    if board.is_game_over():
        display_game_over_message(board)
        break  # Exit the game loop after displaying the result

pygame.quit()
