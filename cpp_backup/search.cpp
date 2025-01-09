
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



std::pair<int16_t , chess::Move> minimax(Board& board, int depth, int16_t alpha, int16_t beta, bool is_maximizing) {
    auto [game_result_reason, game_result] = board.isGameOver();
    if (depth == 0 || (game_result_reason != GameResultReason::NONE)) {
        return {evaluate_board(board), NULL};
    }
    chess::Move best_move = NULL;
    Movelist moves;
    movegen::legalmoves(moves, board);
    sortMovelist(board, moves);
    if (is_maximizing) {
        int16_t max_eval = NEGATIVEINFINITY;
        for (const Move& move : moves) {
            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, false);
            board.unmakeMove(move);
            if (eval > max_eval) {
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
        int16_t min_eval = INFINITY;
        for (const chess::Move& move : moves) {
            board.makeMove(move);
            auto [eval, _] = minimax(board, depth - 1, alpha, beta, true);
            board.unmakeMove(move);
            if (eval < min_eval) {
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


