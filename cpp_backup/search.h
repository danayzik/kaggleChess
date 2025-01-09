#ifndef SEARCH_H
#define SEARCH_H

#include "chess.hpp"
using namespace chess;

bool isCheckMove(Board& board, const Move& move);
void sortMovelist(Board& board, Movelist& moves);
std::pair<int16_t, chess::Move> minimax(Board& board, int depth, int16_t alpha, int16_t beta, bool is_maximizing);

#endif // SEARCH_H
