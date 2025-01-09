#include "chess.hpp"
#include "game_tables.h"
#include "evaluation.h"
#include "search.h"




int main() {
    initTables();
    Board board = Board("r3kbnr/5ppp/1pp1p3/2ppP3/3P4/2P2P2/PP3P1P/RNB2RK1 b kq - 0 11");
    auto [eval, move] = minimax(board, 5, NEGATIVEINFINITY, INFINITY, true);
//    std::cout << evaluate_board(board);
    std::cout << eval;
    return 0;
}