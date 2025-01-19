#include <algorithm>
#include "evaluation.h"
#include "search.h"
#include "transposition_table.cpp"
#include <iostream>
#include <chrono>

TranspositionTable tt(10000, 7000);

uint64_t getTTKey(const Board& board, int depth){
    uint64_t zobrist = board.hash();
    uint64_t shiftedDepth = static_cast<uint64_t>(depth) << 1;
    return zobrist ^ shiftedDepth;
}

bool isCheckMove(Board& board, const Move& move) {
    board.makeMove(move);
    bool isCheck = board.inCheck();
    board.unmakeMove(move);
    return isCheck;
}

void addTTEntry(const Board& board, int eval, Move bestMove, int depth){
    uint64_t key = getTTKey(board, depth);
    TTEntry entry(eval, bestMove, depth, board.fullMoveNumber());
    tt.store(key, entry);
}

std::pair<GameResultReason, GameResult> isGameOver(const Board& board, const Movelist& legalMovelist)  {
    if (board.isHalfMoveDraw()) return board.getHalfMoveDrawType();
    if (board.isInsufficientMaterial()) return {GameResultReason::INSUFFICIENT_MATERIAL, GameResult::DRAW};
    if (board.isRepetition()) return {GameResultReason::THREEFOLD_REPETITION, GameResult::DRAW};
    if (legalMovelist.empty()) {
        if (board.inCheck()) return {GameResultReason::CHECKMATE, GameResult::LOSE};
        return {GameResultReason::STALEMATE, GameResult::DRAW};
    }

    return {GameResultReason::NONE, GameResult::NONE};
}

void sortMovelist(Board& board, Movelist& moves) {
    auto mvvLvaScore = [&board](const Move& move) {
        Square from = move.from();
        Square to = move.to();
        int attacker = static_cast<int>(board.at(from).type());
        int victim = static_cast<int>(board.at(to).type());
        return victim * 10 - attacker;
    };

    auto comparator = [&board, &mvvLvaScore](const Move &a, const Move &b) {
        bool leftIsCheckMove = isCheckMove(board, a);
        bool rightIsCheckMove = isCheckMove(board, b);
        bool leftIsCapture = board.isCapture(a);
        bool rightIsCapture = board.isCapture(b);
        if (leftIsCheckMove && !rightIsCheckMove) return true;
        if (!leftIsCheckMove && rightIsCheckMove) return false;

        if (leftIsCapture && rightIsCapture) {
            return mvvLvaScore(a) > mvvLvaScore(b);
        }

        if (leftIsCapture && !rightIsCapture) return true;
        if (!leftIsCapture && rightIsCapture) return false;
        return false;
    };
    std::sort(moves.begin(), moves.end(), comparator);
}

std::pair<int , Move> iterativeSearch(Board& board, bool is_maximizing, int maxDepth){
    int eval = 0;
    Move bestMove = Move();
    std::pair<int, Move> miniMaxRes;

    for (int depth = 1; depth <= maxDepth; depth++) {
        auto start = std::chrono::high_resolution_clock::now();
        miniMaxRes = minimax(board, depth, NEGINF, INF, is_maximizing);
        eval = miniMaxRes.first;
        bestMove = miniMaxRes.second;
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Elapsed time for depth: " << depth<<" " << duration.count() << " microseconds" << std::endl;
    }

    return {eval, bestMove};
}




std::pair<int , Move> minimax(Board& board, int depth, int alpha, int beta, bool is_maximizing) {

    uint64_t key = getTTKey(board, depth);
    if (tt.hasKey(key)){
        return tt.fetch(key);
    }
    Movelist moves;
    movegen::legalmoves(moves, board);
    auto [resultReason, gameResult] = isGameOver(board, moves);
    if (depth == 0 || (resultReason != GameResultReason::NONE)) {
        return {evaluate_board(board, gameResult, resultReason), Move()};
    }

    Move best_move = Move();
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
        addTTEntry(board, max_eval, best_move, depth);
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
        addTTEntry(board, min_eval, best_move, depth);
        return {min_eval, best_move};
    }
}


