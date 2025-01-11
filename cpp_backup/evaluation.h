#ifndef EVALUATION_H
#define EVALUATION_H

#include "chess.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace chess;

constexpr int INFINITY = 32767;
constexpr int NEGATIVEINFINITY = -32768;
constexpr int castle_rights_bonus = 10;

extern std::map<PieceType, int> ATTACK_VALUES;

extern std::map<PieceType, int> DEFEND_VALUES;

extern std::vector<PieceType> pieces;

int evaluatePieces(const chess::Board& board);
std::vector<Square> getOccupiedSquares(Bitboard bitboard);
int countActiveBits(uint64_t num);
int evaluate_board(const Board& board, GameResult result, GameResultReason reason);
int endgameMateEval(Square whiteKingSquare, Square blackKingSquare, int egPhase, int currEval);
std::pair<GameResultReason, GameResult> gameOver(Board& board);
#endif // EVALUATION_H
