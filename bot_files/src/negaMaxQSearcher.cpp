
#include "../include/transposition_table.h"
#include "../include/searchers.h"
#include "../include/utilities.h"
using namespace bot_utils;
using namespace searchers;
using namespace chess;


negaMaxQSearcher::negaMaxQSearcher(Evaluator* evaluator, bool isWhite)
        : Searcher(evaluator, isWhite, std::make_unique<negaMaxSorter>()) {sorter->setHistoryTable(&historyTable); sorter->setKillerMoves(&killerMoves);}

Move negaMaxQSearcher::getMove(Board &board, int msTimeLimit) {
    searchStartTime = std::chrono::high_resolution_clock::now();
    searchTimeLimit = msTimeLimit;
    return iterativeDeepening(board);
}



Move negaMaxQSearcher::iterativeDeepening(Board &board) {
    int alpha = NEGINF;
    int beta = INF;
    int depth = 1;
    Move pv[MAX_DEPTH] = {};
    stopSearch = false;
    int myMultiplier = isWhite * 2 - 1;
    sorter->setPvLine(pv);
    int eval = 0;
    while(depth < MAX_DEPTH) {
        sorter->setMaxPvDepth(depth-2);
        eval = negaMax(board, depth, 0, alpha, beta, myMultiplier, pv);
        if(stopSearch){
            break;
        }
        depth++;

    }
    decayHistory();
    for (auto& row : killerMoves)
        for (auto& move : row)
            move = Move();
    return pv[0];
}


int negaMaxQSearcher::negaMax(Board &board, int depth, int plyFromRoot, int alpha, int beta, int playerMultiplier,
                             Move *pvLine) {
    auto elapsed = std::chrono::high_resolution_clock::now() - searchStartTime;
    if (elapsed >= std::chrono::milliseconds(searchTimeLimit)) {
        stopSearch = true;
        return 0;
    }
    Movelist moves;
    movegen::legalmoves(moves, board);
    auto [resultReason, gameResult] = isGameOver(board, moves);
    bool gameOver = resultReason != GameResultReason::NONE;
    if(gameOver){
        Color winner = board.sideToMove() == Color::WHITE ? Color::BLACK : Color::WHITE;
        evaluator->setGameOver(gameResult == GameResult::DRAW, winner);
        return evaluator->getEval(board) * playerMultiplier;
    }
    if(depth == 0) {
        return quiesce(board, plyFromRoot + 1, alpha, beta, playerMultiplier);
    }
    Move childPV[MAX_DEPTH];
    sorter->setDepths(depth, plyFromRoot);
    sorter->sortMovelist(board, moves);
    int max_eval = NEGINF - 1;
    for (auto& move: moves) {
        board.makeMove(move);
        int eval = -negaMax(board, depth - 1, plyFromRoot + 1, -beta, -alpha, playerMultiplier*-1, childPV);
        board.unmakeMove(move);
        if(stopSearch){
            return 0;
        }

        if (eval > max_eval) {
            max_eval = eval;
            pvLine[plyFromRoot] = move;
            std::copy(childPV + plyFromRoot + 1, childPV + plyFromRoot +  depth, pvLine + plyFromRoot + 1);
        }
        alpha = max(alpha, eval);
        if (eval >= beta ) {
            historyTable[board.sideToMove()][move.from().index()][move.to().index()] += depth * depth;
            killerMoves[plyFromRoot][1] = killerMoves[plyFromRoot][0];
            killerMoves[plyFromRoot][0] = move;
            break;
        }
    }
    return max_eval;
}

int negaMaxQSearcher::quiesce(chess::Board &board, int plyFromRoot, int alpha, int beta, int playerMultiplier) {
    auto elapsed = std::chrono::high_resolution_clock::now() - searchStartTime;
    if (elapsed >= std::chrono::milliseconds(searchTimeLimit)) {
        stopSearch = true;
        return 0;
    }


    Movelist legalMoves;

    movegen::legalmoves(legalMoves, board);

    auto [resultReason, gameResult] = isGameOver(board, legalMoves);
    bool gameOver = resultReason != GameResultReason::NONE;
    if(gameOver){
        Color winner = board.sideToMove() == Color::WHITE ? Color::BLACK : Color::WHITE;
        evaluator->setGameOver(gameResult == GameResult::DRAW, winner);
        return evaluator->getEval(board) * playerMultiplier;
    }

    evaluator->setGameOngoing();
    int eval = evaluator->getEval(board) * playerMultiplier;
    if(plyFromRoot >= MAX_DEPTH || eval >= beta){
        return eval;
    }
    int maxEval = eval;
    Movelist moves;
    movegen::legalmoves<movegen::MoveGenType::CAPTURE>(moves, board);
    alpha = max(alpha, maxEval);
    sorter->setDepths(0, plyFromRoot);
    sorter->sortCaptures(board, moves);
//    sorter->setMoveScores(board, moves);
    for (auto& move: moves) {
        board.makeMove(move);
        eval = -quiesce(board,plyFromRoot + 1, -beta, -alpha, playerMultiplier*-1);
        board.unmakeMove(move);
        if(stopSearch){
            return 0;
        }

        if (eval > maxEval) {
            maxEval = eval;
        }
        alpha = max(alpha, eval);
        if (eval >= beta ) {
            killerMoves[plyFromRoot][1] = killerMoves[plyFromRoot][0];
            killerMoves[plyFromRoot][0] = move;
            break;
        }
    }
    return maxEval;
}






