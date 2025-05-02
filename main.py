import argparse
from game_sim.simulation import human_vs_bot, bot_vs_stockfish, run_bot_vs_stockfish

def parse_arguments():
    parser = argparse.ArgumentParser(description="Chess game setup")

    # Add subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode')

    # Subparser for human vs bot
    parser_human = subparsers.add_parser('human', help='Play a game between human and bot')

    # Subparser for stockfish vs bot (with visuals)
    parser_stockfish_visuals = subparsers.add_parser('stockfish-visuals', help='Run bot vs stockfish with visuals')
    parser_stockfish_visuals.add_argument('stockfish_path', type=str, help='Path to the stockfish executable')
    parser_stockfish_visuals.add_argument('--stock_fish_strength', type=int, default=2000, help='Strength of the stockfish bot')


    # Subparser for stockfish vs bot (without visuals)
    parser_stockfish = subparsers.add_parser('stockfish', help='Run bot vs stockfish without visuals')
    parser_stockfish.add_argument('stockfish_path', type=str, help='Path to the stockfish executable')
    parser_stockfish.add_argument('--stock_fish_strength', type=int, default=2000, help='Strength of the stockfish bot')
    parser_stockfish.add_argument('--num_threads', type=int, default=5, help='Number of threads to use')
    parser_stockfish.add_argument('--iterations_per_thread', type=int, default=10, help='Number of games to run per thread')

    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = parse_arguments()
    except Exception as e:
        print("Invalid argument format:", e)
        exit(1)
    if args.mode == 'human':
        human_vs_bot()
    elif args.mode == 'stockfish-visuals':
        bot_vs_stockfish(args.stockfish_path, args.stock_fish_strength, visuals=True)
    elif args.mode == 'stockfish':
        run_bot_vs_stockfish(args.stockfish_path, args.stock_fish_strength, args.num_threads, args.iterations_per_thread)
    else:
        print("Invalid mode selected.")
