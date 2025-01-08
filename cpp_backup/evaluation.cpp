#include "chesslib/include/chess.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace chess;
#include "evaluation.h"

int16_t countActiveBits(uint64_t num) {
    return static_cast<int16_t >(__builtin_popcountll(num));
}
std::vector<Square> getOccupiedSquares(Bitboard bitboard) {
    std::vector<Square> occupiedSquares;
    for (int i = 0; i < 64; ++i) {
        if (bitboard & (1ULL << i)) {
            occupiedSquares.push_back(Square(i));
        }
    }
    return occupiedSquares;
}

int16_t evaluatePawnAttacks(const Board& board, Bitboard pawnBitBoard, Color color){
    Bitboard leftAttacks;
    Bitboard rightAttacks;
    int16_t value = 0;
    if (color == Color::WHITE) {
        leftAttacks = attacks::pawnLeftAttacks<Color::WHITE>(pawnBitBoard);
        rightAttacks = attacks::pawnRightAttacks<Color::WHITE>(pawnBitBoard);
    }
    else{
        leftAttacks = attacks::pawnLeftAttacks<Color::BLACK>(pawnBitBoard);
        rightAttacks = attacks::pawnRightAttacks<Color::BLACK>(pawnBitBoard);
    }
    Color enemy_color = ~color;
    for(PieceType type : pieces){
        Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
        Bitboard friendlyPieceBitboard = board.pieces(type, color);
        Bitboard leftAttackedPieces = enemyPieceBitboard & leftAttacks;
        Bitboard rightAttackedPieces = enemyPieceBitboard & rightAttacks;
        Bitboard leftDefendedPieces = friendlyPieceBitboard & leftAttacks;
        Bitboard rightDefendedPieces = friendlyPieceBitboard & rightAttacks;
        value += countActiveBits(leftAttackedPieces.getBits()) * ATTACK_VALUES[type];
        value += countActiveBits(rightAttackedPieces.getBits()) * ATTACK_VALUES[type];
        value += countActiveBits(leftDefendedPieces.getBits()) * DEFEND_VALUES[type];
        value += countActiveBits(rightDefendedPieces.getBits()) * DEFEND_VALUES[type];
    }
    return value;
}
int16_t evaluateKnightAttacks(const Board& board, Bitboard knightBitBoard, Color color){
    std::vector<Square> knightSquares = getOccupiedSquares(knightBitBoard);
    int16_t value = 0;
    Color enemy_color = ~color;
    for (Square sqr: knightSquares) {
        Bitboard attackedSquares = attacks::knight(sqr);
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
            Bitboard friendlyPieceBitboard = board.pieces(type, color);
            Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
            Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
            value += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
            value += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }
    return value;
}

int16_t evaluateBishopAttacks(const Board& board, Bitboard bishopBitBoard, Color color){
    std::vector<Square> bishopSquares = getOccupiedSquares(bishopBitBoard);
    int16_t value = 0;
    Color enemy_color = ~color;
    Bitboard occupiedBoard = board.occ();
    for (Square sqr: bishopSquares) {
        Bitboard attackedSquares = attacks::bishop(sqr, occupiedBoard);
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
            Bitboard friendlyPieceBitboard = board.pieces(type, color);
            Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
            Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
            value += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
            value += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }
    return value;
}
int16_t evaluateRookAttacks(const Board& board, Bitboard rookBitBoard, Color color){
    std::vector<Square> rookSquares = getOccupiedSquares(rookBitBoard);
    int16_t value = 0;
    Color enemy_color = ~color;
    Bitboard occupiedBoard = board.occ();
    for (Square sqr: rookSquares) {
        Bitboard attackedSquares = attacks::rook(sqr, occupiedBoard);
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
            Bitboard friendlyPieceBitboard = board.pieces(type, color);
            Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
            Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
            value += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
            value += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }
    return value;
}
int16_t evaluateQueenAttacks(const Board& board, Bitboard queenBitBoard, Color color){
    std::vector<Square> queenSquares = getOccupiedSquares(queenBitBoard);
    int16_t value = 0;
    Color enemy_color = ~color;
    Bitboard occupiedBoard = board.occ();
    for (Square sqr: queenSquares) {
        Bitboard attackedSquares = attacks::queen(sqr, occupiedBoard);
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
            Bitboard friendlyPieceBitboard = board.pieces(type, color);
            Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
            Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
            value += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
            value += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }
    return value;
}

int16_t evaluateKingAttacks(const Board& board, Color color){
    Square sqr = board.kingSq(color);
    int16_t value = 0;
    Color enemy_color = ~color;
    Bitboard attackedSquares = attacks::king(sqr);
    for(PieceType type : pieces){
        Bitboard enemyPieceBitboard = board.pieces(type, enemy_color);
        Bitboard friendlyPieceBitboard = board.pieces(type, color);
        Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
        Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
        value += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
        value += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
    }
    return value;
}



int16_t evaluate_board(const Board& board) {
    std::pair<GameResultReason, GameResult> gameOverCheck = board.isGameOver();
    GameResultReason resultReason = gameOverCheck.first;
    if (resultReason == GameResultReason::CHECKMATE) {
        return board.sideToMove() == Color::WHITE
                   ? NEGATIVEINFINITY
                   : INFINITY;
    }
    if (gameOverCheck.second == GameResult::DRAW) {
        return 0.0f;
    }
    std::map<chess::Color, float> scores = {{Color::WHITE, 0.0f}, {Color::BLACK, 0.0f}};
    float castle_rights_bonus = 50.0f;
    Board::CastlingRights rights = board.castlingRights();
    if (rights.has(Color::WHITE)) {
        scores[Color::WHITE] += castle_rights_bonus;
    }
    if (rights.has(Color::BLACK)) {
        scores[Color::BLACK] += castle_rights_bonus;
    }
    for (Color color : {Color::WHITE, Color::BLACK}) {
        float colorScore = 0.0f;
        for (PieceType type : pieces) {
            Bitboard pieceBitboard = board.pieces(type, color);
//            colorScore += evaluatePieces(pieces, type, color);
        }
        scores[color] += colorScore;
    }

    return scores[Color::WHITE] - scores[Color::BLACK];
}