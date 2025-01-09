#ifndef EVALUATION_H
#define EVALUATION_H

#include "chess.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace chess;

constexpr int16_t INFINITY = 32767;
constexpr int16_t NEGATIVEINFINITY = -32768;
constexpr int8_t castle_rights_bonus = 30;

extern std::map<PieceType, int16_t> ATTACK_VALUES;

extern std::map<PieceType, int16_t> DEFEND_VALUES;

extern std::vector<PieceType> pieces;

int16_t evaluatePieces(const chess::Board& board);
std::vector<Square> getOccupiedSquares(Bitboard bitboard);
int16_t countActiveBits(uint64_t num);
int16_t evaluate_board(const Board& board);

#endif // EVALUATION_H
