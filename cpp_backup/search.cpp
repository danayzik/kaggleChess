
#include <algorithm>

#include "evaluation.h"
#include "search.h"




bool isCheckMove(Board& board, const Move& move) {
    board.makeMove(move);
    bool isCheck = board.inCheck();
    board.unmakeMove(move);
    return isCheck;
}


void sortMovelist(Board& board, Movelist& moves) {
    auto comparator = [&board](const Move &a, const Move &b) {
        if (isCheckMove(board, a) && !isCheckMove(board, b)) return true;
        if (!isCheckMove(board, a) && isCheckMove(board, b)) return false;

        if (board.isCapture(a) && !board.isCapture(b)) return true;
        if (!board.isCapture(a) && board.isCapture(b)) return false;

        return false;
    };
    std::sort(moves.begin(), moves.end(), comparator);

}



std::pair<int , Move> minimax(Board& board, int depth, int alpha, int beta, bool is_maximizing) {
    GameResultReason game_result_reason;
    GameResult game_result;
    std::pair<GameResultReason, GameResult> gameOverCheck;
    gameOverCheck = board.isGameOver();
    game_result_reason = gameOverCheck.first;
    game_result = gameOverCheck.second;
    if (depth == 0 || (game_result_reason != GameResultReason::NONE)) {
        return {evaluate_board(board, game_result, game_result_reason), Move()};
    }
    chess::Move best_move = Move();
    Movelist moves;
    movegen::legalmoves(moves, board);
    sortMovelist(board, moves);
    if (is_maximizing) {
        int max_eval = NEGINF-1;
        for (auto move : moves) {
            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, false);
            board.unmakeMove(move);
            if (eval > max_eval) {
                best_move = move;
            }
            max_eval = std::max(eval, max_eval);
            alpha = std::max(alpha, eval);
            if (eval >= beta) {
                break;
            }
        }
        return {max_eval, best_move};

    }
    else {
        int min_eval = INF+1;
        for (auto move : moves) {
            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, true);
            board.unmakeMove(move);
            if (eval < min_eval) {
                best_move = move;
            }
            min_eval = std::min(min_eval, eval);
            beta = std::min(beta, eval);
            if (eval <= alpha) {
                break;
            }
        }
        return {min_eval, best_move};
    }
}


