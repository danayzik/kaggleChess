import chess.pgn
import csv
from evaluator import Evaluator, StaticStockfishEvaluator
import os

def process_pgn_file():
    input_pgn = r"D:\downloads\sep2019"
    output_dir = r"D:\chess\dataDepth0"
    game_count = 0
    file_count = 1

    def create_new_csv():
        """Helper function to create a new CSV file."""
        file_name = os.path.join(output_dir, f"data{file_count}.csv")
        csv_file = open(file_name, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["FEN", "Evaluation"])
        return csv_file, csv_writer

    evaluator = StaticStockfishEvaluator()
    pgn = open(input_pgn, 'r')
    csv_file, csv_writer = create_new_csv()

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            fen = board.fen()
            eval_score = evaluator.get_eval(fen)
            if -1000 <= eval_score <= 1000:
                csv_writer.writerow([fen, eval_score])

        game_count += 1

        if game_count % 100 == 0:
            csv_file.close()
            file_count += 1
            csv_file, csv_writer = create_new_csv()

    csv_file.close()
    evaluator.quit()
    pgn.close()

