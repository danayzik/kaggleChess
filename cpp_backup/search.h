#ifndef SEARCH_H
#define SEARCH_H

#include "chess.hpp"
using namespace chess;

bool isCheckMove(Board& board, const Move& move);
void sortMovelist(Board& board, Movelist& moves);
std::pair<int , chess::Move> minimax(Board& board, int depth, int alpha, int beta, bool is_maximizing);

#endif // SEARCH_H
