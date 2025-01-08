#include "chesslib/include/chess.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace chess;
#include "evaluation.h"

#ifndef UNTITLED_EVALUATION_H
#define UNTITLED_EVALUATION_H

const std::map<PieceType, int16_t> PIECE_VALUES = {
    {PieceType::PAWN, 100},
    {PieceType::KNIGHT, 300},
    {PieceType::BISHOP, 330},
    {PieceType::ROOK, 500},
    {PieceType::QUEEN, 900},
    {PieceType::KING, 0}
};

std::map<PieceType, int16_t> ATTACK_VALUES = {
    {PieceType::PAWN, 5},
    {PieceType::KNIGHT, 1},
    {PieceType::BISHOP, 1},
    {PieceType::ROOK, 2},
    {PieceType::QUEEN, 3},
    {PieceType::KING, 5}
};

std::map<PieceType, int16_t> DEFEND_VALUES = {
    {PieceType::PAWN, 20},
    {PieceType::KNIGHT, 10},
    {PieceType::BISHOP, 10},
    {PieceType::ROOK, 5},
    {PieceType::QUEEN, 0},
    {PieceType::KING, 0}
};

std::vector<PieceType> pieces = {
    PieceType::PAWN,
    PieceType::KNIGHT,
    PieceType::BISHOP,
    PieceType::ROOK,
    PieceType::QUEEN,
    PieceType::KING
};

class evaluation {

};


#endif //UNTITLED_EVALUATION_H
