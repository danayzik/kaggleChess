
#include <algorithm>
#include <map>
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




std::pair<int , chess::Move> minimax(Board& board, int depth, int alpha, int beta, bool is_maximizing, bool inSearch) {
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
        int max_eval = NEGATIVEINFINITY;
        for (const Move& move : moves) {
            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, false, true);
            board.unmakeMove(move);
            if (eval >= max_eval) {
                max_eval = eval;
                best_move = move;
            }
            alpha = std::max(alpha, eval);
            if (beta <= alpha) {
                break;
            }
        }
        return {max_eval, best_move};

    } else {
        int min_eval = INFINITY;
        for (const chess::Move& move : moves) {

            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, true, true);
            board.unmakeMove(move);
            if (eval <= min_eval) {
                min_eval = eval;
                best_move = move;
            }
            beta = std::min(beta, eval);
            if (beta <= alpha) {
                break;
            }
        }
        return {min_eval, best_move};
    }
}


