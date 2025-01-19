#include <algorithm>
#include "evaluation.h"
#include "search.h"
#include "transposition_table.cpp"
#include <iostream>
#include <chrono>

TranspositionTable tt(10000, 7000);
Move pv_move = Move();
int currDepth = -1;
std::vector<std::vector<std::vector<int>>> historyTable(2, std::vector<std::vector<int>>(6, std::vector<int>(64, 0)));

uint64_t getTTKey(Board& board, int depth){
    uint64_t zobrist = board.hash();
    uint64_t shiftedDepth = static_cast<uint64_t>(depth) << 1;
    return zobrist ^ shiftedDepth;
}

void updateHistory(Board& board, const Move& move, int depth, bool isWhite){
    int side = !isWhite;
    int piece = static_cast<int>(board.at(move.from()).type());
    int sqr = move.to().index();
    historyTable[side][piece][sqr] += depth*depth;
}

bool isCheckMove(Board& board, const Move& move) {
    board.makeMove(move);
    bool isCheck = board.inCheck();
    board.unmakeMove(move);
    return isCheck;
}

int fetchHistoryScore(Board& board,Move move){
    int side = static_cast<int>(board.sideToMove());
    int piece = static_cast<int>(board.at(move.from()).type());
    int sqr = move.to().index();
    return historyTable[side][piece][sqr];
}

bool isHashMove(Board& board, const Move& move){
    board.makeMove(move);
    uint64_t key = getTTKey(board, currDepth);
    board.unmakeMove(move);
    return tt.hasKey(key);
}

void addTTEntry(Board& board, int eval, Move bestMove, int depth){
    uint64_t key = getTTKey(board, depth);
    TTEntry entry(eval, bestMove, depth, board.fullMoveNumber());
    tt.store(key, entry);
}

std::pair<GameResultReason, GameResult> isGameOver(Board& board, Movelist& legalMovelist)  {
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
    auto isLosingCapture = [&board](const Move& move){
        Square from = move.from();
        Square to = move.to();
        std::map<PieceType, int> valueMap = {
                {PieceType::PAWN , 1},
                {PieceType::KNIGHT , 2},
                {PieceType::BISHOP , 2},
                {PieceType::ROOK , 3},
                {PieceType::QUEEN , 4},
                {PieceType::KING , 0}
        };
        PieceType attacker = board.at(from).type();
        PieceType victim = board.at(to).type();
        return (valueMap[victim] - valueMap[attacker]) < 0;
    };

    auto comparator = [&board, &mvvLvaScore, &isLosingCapture](const Move &a, const Move &b) {
        bool leftIsPV = a == pv_move;
        bool rightIsPV = b == pv_move;
        if (leftIsPV && !rightIsPV) return true;
        if (!leftIsPV && rightIsPV) return false;
        bool leftIsHash = isHashMove(board, a);
        bool rightIsHash = isHashMove(board, b);
        if (leftIsHash && !rightIsHash) return true;
        if (!leftIsHash && rightIsHash) return false;
        bool leftIsCheckMove = isCheckMove(board, a);
        bool rightIsCheckMove = isCheckMove(board, b);
        if (leftIsCheckMove && !rightIsCheckMove) return true;
        if (!leftIsCheckMove && rightIsCheckMove) return false;
        bool leftIsCapture = board.isCapture(a);
        bool rightIsCapture = board.isCapture(b);
        if(leftIsCapture && rightIsCapture){
            bool leftIsLosing = isLosingCapture(a);
            bool rightIsLosing = isLosingCapture(b);
            if (leftIsLosing && !rightIsLosing)
                return false;
            if(!leftIsLosing && rightIsLosing)
                return true;
            return mvvLvaScore(a) > mvvLvaScore(b);
        }
        if(leftIsCapture && !rightIsCapture){
            if(isLosingCapture(a))
                return false;
            return true;
        }
        if(!leftIsCapture && rightIsCapture){
            if(isLosingCapture(b))
                return true;
            return false;
        }
        return fetchHistoryScore(board, a) > fetchHistoryScore(board, b);
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
        auto end = std::chrono::high_resolution_clock::now();
        eval = miniMaxRes.first;
        bestMove = miniMaxRes.second;
        pv_move = bestMove;
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Elapsed time for depth: " << depth<<" " << duration.count() << " microseconds" << std::endl;
    }

    return {eval, bestMove};
}




std::pair<int , Move> minimax(Board& board, int depth, int alpha, int beta, bool is_maximizing) {
    currDepth = depth;
    Movelist moves;
    movegen::legalmoves(moves, board);
    auto [resultReason, gameResult] = isGameOver(board, moves);
    if (depth == 0 || (resultReason != GameResultReason::NONE)) {
        return {evaluate_board(board, gameResult, resultReason), Move()};
    }
    uint64_t key = getTTKey(board, depth);
    if (tt.hasKey(key)){
        return tt.fetch(key);
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
                if (!board.isCapture(move))
                    updateHistory(board, move, depth, is_maximizing);
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
                if (!board.isCapture(move))
                    updateHistory(board, move, depth, is_maximizing);
                break;
            }
        }
        addTTEntry(board, min_eval, best_move, depth);
        return {min_eval, best_move};
    }
}


